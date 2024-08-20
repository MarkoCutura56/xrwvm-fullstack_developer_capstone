FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

ENV APP=/home/project/xrwvm-fullstack_developer_capstone/server

# Change the workdir.
WORKDIR $APP

# Install the requirements
COPY requirements.txt $APP

RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY . $APP

EXPOSE 8000

RUN chmod +x /home/project/xrwvm-fullstack_developer_capstone/server/entrypoint.sh

ENTRYPOINT ["/bin/bash","/home/project/xrwvm-fullstack_developer_capstone/server/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]