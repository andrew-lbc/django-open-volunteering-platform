from functools import wraps
import json

def dump_to_file(content):
  with open("/tmp/debug_dump.txt", "a") as f:
    f.write("{}\n=============\n".format(content))

def debug_dump_request(function):

  @wraps(function)
  def wrapper(self, *args, **kwargs):
    request = args[0]
    response = function(self, *args, **kwargs)
    content = "In: {url}\nBody: {request_body}\n\nOut: {status}\nBody: {response_body}".format(
      url = request.build_absolute_uri(),
      request_body = json.dumps(request.data),
      status = response.status_code,
      response_body = json.dumps(response.data)
    )
    dump_to_file(content)

    return response

  return wrapper
