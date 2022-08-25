#
# See https://hub.docker.com/_/python
#
# Also https://vsupalov.com/docker-shared-permissions/
# 
# To use -
#
# $ docker build -t my-python-app --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
#
# N.B. must pass in sound device
# $ docker run -it --rm --device /dev/snd -v ${PWD}:/usr/src/app --name my-running-app my-python-app

FROM python:3.9
WORKDIR /usr/src/app


ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user

# Our app uses audio, so add audio support to the container.
RUN apt update -y;apt install -y portaudio19-dev python3-pyaudio

USER user

# We are going to be checking our app for linting errors and running unit tests.
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade pytest pytest-cov pytest-socket flake8 flake8-junit-report

# NB The scripts pytest, flake8 etc are installed in '/home/user/.local/bin'
# So add this to PATH
ENV PATH=/home/user/.local/bin:$PATH

# To install requirements on build use
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# To copy our app on build use
# COPY . .
# Alternative is to mount PWD wth command line option 
# -v ${PWD}:/usr/src/app

# CMD flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics 2>&1 ; \
CMD pip install --no-cache-dir -r requirements.txt ; \
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics  --output-file flake8.txt ; \
flake8_junit flake8.txt flake8.xml; \
cat flake8.txt; \
echo "-----"; \
pytest --cov=. .;

# CMD python ./main.py