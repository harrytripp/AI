from openai import OpenAI
client = OpenAI()
i = 1
firstMessage = True

# Create the Assistant
assistant = client.beta.assistants.create(
  name="Salesman",
  instructions="Strengthen the given instructions to make them more assertive and direct. Emphasize your role in showcasing the strengths of Harry Tripp, an IT Technician. Leverage the files provided to comprehensively address any questions about his capabilities. Be prepared to answer inquiries from recruiters, hiring managers, HR staff, and technical leaders. Respond confidently and provide detailed, persuasive answers to highlight Harry's qualifications effectively.",
  tools=[{"type": "file_search"}],
  model="gpt-4o-mini",
)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Financial Statements")

# Ready the files for upload to OpenAI
file_paths = ["./profile.txt", "./tech_stack_and_skills.txt", "professional_experience.txt"]
file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)

# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# Create a Thread
thread = client.beta.threads.create()

while i == 1:
  # Add a Message to the Thread
  if firstMessage == True:
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=input("Hello, I am an AI Assistant. (Disclaimer: I am liable to make mistakes.)\n\nAsk me about Harry!\n")
  )
    firstMessage = False
  else:
    # The Message must not be empty - this prevents sending an invalid request.
    userInput = ""
    while userInput == "":
      userInput = input()
    if userInput != "":
      message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content = userInput
    )

  from typing_extensions import override
  from openai import AssistantEventHandler

  # First, we create a EventHandler class to define
  # how we want to handle the events in the response stream.

  class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
      print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
      print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
      print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
      if delta.type == 'code_interpreter':
        if delta.code_interpreter.input:
          print(delta.code_interpreter.input, end="", flush=True)
        if delta.code_interpreter.outputs:
          print(f"\n\noutput >", flush=True)
          for output in delta.code_interpreter.outputs:
            if output.type == "logs":
              print(f"\n{output.logs}", flush=True)

  # Then, we use the `stream` SDK helper 
  # with the `EventHandler` class to create the Run 
  # and stream the response.

  with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Start the interaction with a polite and friendly greeting. Kindly ask the user for their name. Use this name in all subsequent interactions to make the conversation more personal and respectful.",
    event_handler=EventHandler(),
  ) as stream:
    stream.until_done()

  if i != 1:
    break