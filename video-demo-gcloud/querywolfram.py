import requests
import xmltodict

"""
Parameters for Wolfram Alpha Query
"""


class config:
    # Query Parameters
    query_url = "http://api.wolframalpha.com/v2/query"
    query_params = {
        # This is where you put the question you want to ask it
        "input": "how fast can a cheetah run",
        # This is the App ID provided via your Wolfram Alpha developer account
        "appid": "AH3JX3-L23R5H2793",
        # This means we only get the result and not the rest of the response.
        "includepodid": "Result"
    }

    # Response locations in the returned xml (when using the 'Result' setting,
    # above)
    success_response_location = ['queryresult', '@success']
    failure_response_location = ['queryresult', 'error', 'msg']
    plain_text_response_location = [
        'queryresult', 'pod', 'subpod', 'plaintext']


# Utility for navigating dictionaries to given location
def get_item(location, source):
    """This retrieves the data at a given location in the xml tree, if it is present.
    TODO Possibly a better way to do this would be to iterate through the tree looking for it,
    as I'm not sure how reliable the exact structure is. Probably the tags are reliable but the exact
    structure isn't."""
    subset = source
    try:
        for subscript in location:
            subset = subset[subscript]
        return subset
    except KeyError:
        return None


def answer_query(question: str) -> str:

    config.query_params["input"] = question
    # Do the query
    response = requests.get(config.query_url, config.query_params)

    if not response.ok:
        # Query was not successful
        print(response, response.content)
        return "Sorry, I don't have an answer for that question."
    else:
        # Query was successful
        # TODO Sometimes it asks for 'userinfo' (e.g. if you ask what time it is, it will ask you for your time zone).
        # In this situation it currently returns None. We would ideally catch
        # this and ask for more user input.
        response_dict = xmltodict.parse(response.text)
        response_for_reading = get_item(
            config.plain_text_response_location, response_dict)
        # print(response_dict)
        return response_for_reading


if __name__ == '__main__':

    while True:
        # Get the user input
        question = input("Waiting for your question...\n> ")

        if question in ["quit", "exit", "close"]:
            print("Thank you")
            break

        answer = answer_query(question)
        print(answer)
