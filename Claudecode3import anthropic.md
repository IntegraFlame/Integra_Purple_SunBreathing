import anthropic

# uses ANTHROPIC_API_KEY or credentials from `ant auth login`
client = anthropic.Anthropic()

message_batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "first-prompt-in-my-batch",
            "params": {
                "model": "claude-haiku-5-5",
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hey Claude, tell me a short fun fact about video games!",
                    }
                ],
            },
        },
        {
            "custom_id": "second-prompt-in-my-batch",
            "params": {
                "model": "claude-sonnet-5-5",
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hey Claude, tell me a short fun fact about bees!",
                    }
                ],
            },
        },
    ]
)
print(message_batch)---


title: Batch processing
url: https://platform.claude.com/docs/en/build-with-claude/batch-processing
description: Process large volumes of Messages requests asynchronously with the Message Batches API, cutting costs by 50% and increasing throughput.
---

Batch processing is a powerful approach for handling large volumes of requests efficiently. Instead of processing requests one at a time with immediate responses, batch processing allows you to submit multiple requests together for asynchronous processing. This pattern is particularly useful when:

* You need to process large volumes of data
* Immediate responses are not required
* You want to optimize for cost efficiency
* You're running large-scale evaluations or analyses

The Message Batches API is Anthropic's first implementation of this pattern.

<Note>
  To learn how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

# Message Batches API

The Message Batches API is a powerful, cost-effective way to asynchronously process large volumes of [Messages](https://platform.claude.com/docs/en/api/messages/create) requests. This approach is well-suited to tasks that do not require immediate responses, with most batches finishing in less than 1 hour while reducing costs by 50% and increasing throughput.

You can [explore the API reference directly](https://platform.claude.com/docs/en/api/messages/batches/create), in addition to this guide.

## How the Message Batches API works

When you send a request to the Message Batches API:

1. The system creates a new Message Batch with the provided Messages requests.
2. The batch is then processed asynchronously, with each request handled independently.
3. You can poll for the status of the batch and retrieve results when processing has ended for all requests.

This is especially useful for bulk operations that don't require immediate results, such as:

* Large-scale evaluations: Process thousands of test cases efficiently.
* Content moderation: Analyze large volumes of user-generated content asynchronously.
* Data analysis: Generate insights or summaries for large datasets.
* Bulk content generation: Create large amounts of text for various purposes (for example, product descriptions, article summaries).

### Batch limitations

* A Message Batch is limited to either 100,000 Message requests or 256 MB in size, whichever is reached first.
* The system processes each batch as fast as possible, with most batches completing within 1 hour. You can access batch results when all messages have completed or after 24 hours, whichever comes first. Batches expire if processing does not complete within 24 hours.
* Batch results are available for 29 days after creation. After that, you may still view the Batch, but its results will no longer be available for download.
* Batches are scoped to a [Workspace](https://platform.claude.com/settings/workspaces). You may view all batches (and their results) that were created within the Workspace your request runs in.
* Rate limits apply to both Batches API HTTP requests and the number of requests within a batch waiting to be processed. See [Message Batches API rate limits](https://platform.claude.com/docs/en/api/rate-limits#message-batches-api). Additionally, processing may be slowed down based on current demand and your request volume. In that case, you may see more requests expiring after 24 hours.
* Because of high throughput and concurrent processing, batches may go slightly over your Workspace's configured [spend limit](https://platform.claude.com/settings/billing).
* Each batched request must have `max_tokens` of at least `1`. `max_tokens: 0` ([cache pre-warming](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pre-warming-the-cache)) is not supported inside a batch, because an ephemeral cache entry written during batch processing would likely expire before the follow-up request runs.

### Supported models

All [active models](https://platform.claude.com/docs/en/models/overview) support the Message Batches API.

### What can be batched

Almost any request you can make to the Messages API can be included in a batch. This includes:

* Vision
* Tool use, including all [server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools) (web search, web fetch, code execution, MCP connectors, advisor, and tool search)
* System messages
* Multi-turn conversations
* Extended thinking
* Most beta features

Because each request in the batch is processed independently, you can mix different types of requests within a single batch.

A small number of Messages API parameters are **not** supported in batch requests. Including any of these returns a validation error:

| Parameter                                                                              | Why                                                                                                                |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `stream: true`                                                                         | Batch results come back as a single file, not a stream.                                                            |
| `speed` ([Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode)) | Fast mode tunes synchronous latency, which doesn't apply to asynchronous batch processing.                         |
| `max_tokens: 0`                                                                        | See [Batch limitations](https://platform.claude.com/docs/en/build-with-claude/batch-processing#batch-limitations). |

<Tip>
  Because batches can take longer than 5 minutes to process, consider using the [1-hour cache duration](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration) with prompt caching for better cache hit rates when processing batches with shared context.
</Tip>

## Pricing

The Batches API offers significant cost savings. All usage is charged at 50% of the standard API prices.

| Model                                                                                                                                | Batch input  | Batch output  |
| :----------------------------------------------------------------------------------------------------------------------------------- | :----------- | :------------ |
| Claude Fable 5.1                                                                                                                     | $5 / MTok    | $25 / MTok    |
| Claude Mythos 5.1 ([limited availability](https://support.claude.com/en/articles/14604842))                                          | $5 / MTok    | $25 / MTok    |
| Claude Fable 5                                                                                                                       | $5 / MTok    | $25 / MTok    |
| Claude Mythos 5 ([limited availability](https://support.claude.com/en/articles/14604842))                                            | $5 / MTok    | $25 / MTok    |
| Claude Opus 5.5                                                                                                                      | $2 / MTok    | $10 / MTok    |
| Claude Opus 5                                                                                                                        | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.8                                                                                                                      | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.7                                                                                                                      | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.6                                                                                                                      | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.5                                                                                                                      | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.1 ([retired, except on Bedrock and Google Cloud](https://platform.claude.com/docs/en/about-claude/model-deprecations)) | $7.50 / MTok | $37.50 / MTok |
| Claude Opus 4 ([retired, except on Google Cloud](https://platform.claude.com/docs/en/about-claude/model-deprecations))               | $7.50 / MTok | $37.50 / MTok |
| Claude Sonnet 5.5                                                                                                                    | $1 / MTok    | $5 / MTok     |
| Claude Sonnet 5                                                                                                                      | $1 / MTok    | $5 / MTok     |
| Claude Sonnet 4.6                                                                                                                    | $1.50 / MTok | $7.50 / MTok  |
| Claude Sonnet 4.5                                                                                                                    | $1.50 / MTok | $7.50 / MTok  |
| Claude Sonnet 4 ([retired, except on Bedrock and Google Cloud](https://platform.claude.com/docs/en/about-claude/model-deprecations)) | $1.50 / MTok | $7.50 / MTok  |
| Claude Haiku 5.5 (for prompts up to 100,000 tokens)                                                                                  | $0.05 / MTok | $0.25 / MTok  |
| Claude Haiku 5.5 (for prompts over 100,000 tokens)                                                                                   | $0.25 / MTok | $1.25 / MTok  |
| Claude Haiku 4.5                                                                                                                     | $0.50 / MTok | $2.50 / MTok  |
| Claude Haiku 3.5 ([retired, except on Google Cloud](https://platform.claude.com/docs/en/about-claude/model-deprecations))            | $0.40 / MTok | $2 / MTok     |

* **MTok:** Million tokens. $5 / MTok is $5 for every million tokens.
* **Limited access:** Available only to organizations verified through Anthropic’s verification programs, such as the [Cyber Verification Program](https://support.claude.com/en/articles/14604842). To request access, apply to the program that covers your use case.
* **Retired:** May still be available on other cloud platforms. See [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) for more.

## How to use the Message Batches API

### Prepare and create your batch

A Message Batch is composed of a list of requests to create a Message. The shape of an individual request comprises:

* A unique `custom_id` for identifying the Messages request. Must be 1 to 64 characters and contain only alphanumeric characters, hyphens, and underscores (matching `^[a-zA-Z0-9_-]{1,64}$`).
* A `params` object with the standard [Messages API](https://platform.claude.com/docs/en/api/messages/create) parameters

You can [create a batch](https://platform.claude.com/docs/en/api/messages/batches/create) by passing this list into the `requests` parameter:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/batches \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data \
  '{
      "requests": [
          {
              "custom_id": "my-first-request",
              "params": {
                  "model": "claude-opus-5-5",
                  "max_tokens": 1024,
                  "messages": [
                      {"role": "user", "content": "Hello, world"}
                  ]
              }
          },
          {
              "custom_id": "my-second-request",
              "params": {
                  "model": "claude-opus-5-5",
                  "max_tokens": 1024,
                  "messages": [
                      {"role": "user", "content": "Hi again, friend"}
                  ]
              }
          }
      ]
  }'
  ```

  ```bash CLI
  ant messages:batches create <<'YAML'
  requests:
    - custom_id: my-first-request
      params:
        model: claude-opus-5-5
        max_tokens: 1024
        messages:
          - role: user
            content: Hello, world
    - custom_id: my-second-request
      params:
        model: claude-opus-5-5
        max_tokens: 1024
        messages:
          - role: user
            content: Hi again, friend
  YAML
  ```

  ```python Python
  from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
  from anthropic.types.messages.batch_create_params import Request

  client = anthropic.Anthropic()

  message_batch = client.messages.batches.create(
      requests=[
          Request(
              custom_id="my-first-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-opus-5-5",
                  max_tokens=1024,
                  messages=[
                      {
                          "role": "user",
                          "content": "Hello, world",
                      }
                  ],
              ),
          ),
          Request(
              custom_id="my-second-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-opus-5-5",
                  max_tokens=1024,
                  messages=[
                      {
                          "role": "user",
                          "content": "Hi again, friend",
                      }
                  ],
              ),
          ),
      ]
  )

  print(message_batch)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const messageBatch = await client.messages.batches.create({
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          messages: [{ role: "user", content: "Hello, world" }]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          messages: [{ role: "user", content: "Hi again, friend" }]
        }
      }
    ]
  });

  console.log(messageBatch);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;
  using Anthropic.Models.Messages.Batches;

  AnthropicClient client = new();

  var batch = await client.Messages.Batches.Create(new BatchCreateParams
  {
      Requests =
      [
          new()
          {
              CustomID = "my-first-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus5_5,
                  MaxTokens = 1024,
                  Messages =
                  [
                      new() { Role = Role.User, Content = "Hello, world" }
                  ]
              }
          },
          new()
          {
              CustomID = "my-second-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus5_5,
                  MaxTokens = 1024,
                  Messages =
                  [
                      new() { Role = Role.User, Content = "Hi again, friend" }
                  ]
              }
          }
      ]
  });

  Console.WriteLine(batch);
  ```

  ```go Go
  client := anthropic.NewClient()

  batch, _ := client.Messages.Batches.New(context.Background(),
  	anthropic.MessageBatchNewParams{
  		Requests: []anthropic.MessageBatchNewParamsRequest{
  			{
  				CustomID: "my-first-request",
  				Params: anthropic.MessageBatchNewParamsRequestParams{
  					Model:     anthropic.ModelClaudeOpus5_5,
  					MaxTokens: 1024,
  					Messages: []anthropic.MessageParam{
  						anthropic.NewUserMessage(
  							anthropic.NewTextBlock("Hello, world"),
  						),
  					},
  				},
  			},
  			{
  				CustomID: "my-second-request",
  				Params: anthropic.MessageBatchNewParamsRequestParams{
  					Model:     anthropic.ModelClaudeOpus5_5,
  					MaxTokens: 1024,
  					Messages: []anthropic.MessageParam{
  						anthropic.NewUserMessage(
  							anthropic.NewTextBlock("Hi again, friend"),
  						),
  					},
  				},
  			},
  		},
  	})

  fmt.Println(batch.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BatchCreateParams params = BatchCreateParams.builder()
    .addRequest(
      BatchCreateParams.Request.builder()
        .customId("my-first-request")
        .params(
          BatchCreateParams.Request.Params.builder()
            .model(Model.CLAUDE_OPUS_5_5)
            .maxTokens(1024)
            .addUserMessage("Hello, world")
            .build()
        )
        .build()
    )
    .addRequest(
      BatchCreateParams.Request.builder()
        .customId("my-second-request")
        .params(
          BatchCreateParams.Request.Params.builder()
            .model(Model.CLAUDE_OPUS_5_5)
            .maxTokens(1024)
            .addUserMessage("Hi again, friend")
            .build()
        )
        .build()
    )
    .build();

  MessageBatch messageBatch = client.messages().batches().create(params);

  System.out.println(messageBatch);
  ```

  ```php PHP
  $client = new Client();

  $batch = $client->messages->batches->create(
      requests: [
          [
              'custom_id' => 'my-first-request',
              'params' => [
                  'model' => 'claude-opus-5-5',
                  'max_tokens' => 1024,
                  'messages' => [
                      ['role' => 'user', 'content' => 'Hello, world']
                  ]
              ]
          ],
          [
              'custom_id' => 'my-second-request',
              'params' => [
                  'model' => 'claude-opus-5-5',
                  'max_tokens' => 1024,
                  'messages' => [
                      ['role' => 'user', 'content' => 'Hi again, friend']
                  ]
              ]
          ]
      ],
  );

  echo $batch->id;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  batch = client.messages.batches.create(
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          messages: [
            { role: "user", content: "Hello, world" }
          ]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          messages: [
            { role: "user", content: "Hi again, friend" }
          ]
        }
      }
    ]
  )

  puts batch
  ```
</CodeGroup>

In this example, two separate requests are batched together for asynchronous processing. Each request has a unique `custom_id` and contains the standard parameters you'd use for a Messages API call.

<Tip>
  **Test your batch requests with the Messages API**

  Validation of the `params` object for each message request is performed asynchronously, and validation errors are returned when processing of the entire batch has ended. You can ensure that you are building your input correctly by verifying your request shape with the [Messages API](https://platform.claude.com/docs/en/api/messages/create) first.
</Tip>

When a batch is first created, the response has a processing status of `in_progress`.

```json Output
{
  "id": "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
  "type": "message_batch",
  "processing_status": "in_progress",
  "request_counts": {
    "processing": 2,
    "succeeded": 0,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "ended_at": null,
  "created_at": "2024-09-24T18:37:24.100435Z",
  "expires_at": "2024-09-25T18:37:24.100435Z",
  "cancel_initiated_at": null,
  "results_url": null
}
```

### Tracking your batch

The Message Batch's `processing_status` field indicates the stage of processing the batch is in. It starts as `in_progress`, then updates to `ended` once all the requests in the batch have finished processing, and results are ready. You can monitor the state of your batch by visiting the [Console](https://platform.claude.com/settings/workspaces/default/batches), or using the [retrieval endpoint](https://platform.claude.com/docs/en/api/messages/batches/retrieve).

#### Polling for Message Batch completion

To poll a Message Batch, you'll need its `id`, which is provided in the response when creating a batch or by listing batches. You can implement a polling loop that checks the batch status periodically until processing has ended:

<CodeGroup>
  ```bash cURL
  #!/bin/sh
  # ...
  # Check the status; repeat until processing_status is "ended"
  curl -s "https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID" \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    | jq -r '.processing_status'
  ```

  ```bash CLI
  #!/bin/bash
  # ...
  # Check the status; repeat until processing_status is "ended"
  ant messages:batches retrieve \
    --message-batch-id "$MESSAGE_BATCH_ID" \
    --transform processing_status --raw-output
  ```

  ```python Python
  import time

  client = anthropic.Anthropic()

  MESSAGE_BATCH_ID = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"

  message_batch = None
  while True:
      message_batch = client.messages.batches.retrieve(MESSAGE_BATCH_ID)
      if message_batch.processing_status == "ended":
          break

      print(f"Batch {MESSAGE_BATCH_ID} is still processing...")
      time.sleep(60)
  print(message_batch)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const messageBatchId = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d";

  let messageBatch;
  while (true) {
    messageBatch = await client.messages.batches.retrieve(messageBatchId);
    if (messageBatch.processing_status === "ended") {
      break;
    }

    console.log(`Batch ${messageBatchId} is still processing... waiting`);
    await new Promise((resolve) => setTimeout(resolve, 60_000));
  }
  console.log(messageBatch);
  ```

  ```csharp C#
  AnthropicClient client = new();
  string messageBatchId = Environment.GetEnvironmentVariable("MESSAGE_BATCH_ID");

  MessageBatch messageBatch = null;
  while (true)
  {
      messageBatch = await client.Messages.Batches.Retrieve(messageBatchId);
      if (messageBatch.ProcessingStatus == "ended")
      {
          break;
      }

      Console.WriteLine($"Batch {messageBatchId} is still processing...");
      await Task.Delay(60000);
  }
  Console.WriteLine(messageBatch);
  ```

  ```go Go
  client := anthropic.NewClient()
  messageBatchID := os.Getenv("MESSAGE_BATCH_ID")

  var messageBatch *anthropic.MessageBatch
  for {
  	var err error
  	messageBatch, err = client.Messages.Batches.Get(context.TODO(), messageBatchID, anthropic.MessageBatchGetParams{})
  	if err != nil {
  		log.Fatal(err)
  	}
  	if messageBatch.ProcessingStatus == "ended" {
  		break
  	}

  	fmt.Printf("Batch %s is still processing...\n", messageBatchID)
  	time.Sleep(60 * time.Second)
  }
  fmt.Println(messageBatch)
  ```

  ```java Java
  import com.anthropic.models.messages.batches.MessageBatch;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();
          String messageBatchId = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d";

          MessageBatch messageBatch = null;
          while (true) {
              messageBatch = client.messages().batches().retrieve(messageBatchId);
              if (messageBatch.processingStatus().equals(MessageBatch.ProcessingStatus.ENDED)) {
                  break;
              }

              System.out.println("Batch " + messageBatchId + " is still processing...");
              Thread.sleep(60000);
          }
          System.out.println(messageBatch);
  ```

  ```php PHP
  $client = new Client();
  $messageBatchId = getenv("MESSAGE_BATCH_ID");

  $messageBatch = null;
  while (true) {
      $messageBatch = $client->messages->batches->retrieve(
          messageBatchID: $messageBatchId,
      );
      if ($messageBatch->processingStatus === "ended") {
          break;
      }

      echo "Batch {$messageBatchId} is still processing...\n";
      sleep(60);
  }
  echo json_encode($messageBatch, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message_batch_id = ENV["MESSAGE_BATCH_ID"]
  message_batch = nil
  loop do
    message_batch = client.messages.batches.retrieve(message_batch_id)
    break if message_batch.processing_status == :ended

    puts "Batch #{message_batch_id} is still processing..."
    sleep 60
  end
  puts message_batch
  ```
</CodeGroup>

### Listing all Message Batches

You can list all Message Batches in your Workspace using the [list endpoint](https://platform.claude.com/docs/en/api/messages/batches/list). The API supports pagination, automatically fetching additional pages as needed:

<CodeGroup>
  ```bash cURL
  #!/bin/sh
  # Fetches one page. While the response's has_more is true, pass its
  # last_id as after_id to fetch the next page. (The SDKs and the CLI
  # perform automatic pagination.)
  curl -s "https://api.anthropic.com/v1/messages/batches?limit=20" \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  # Automatically fetches more pages as needed
  ant messages:batches list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Automatically fetches more pages as needed.
  for message_batch in client.messages.batches.list(limit=20):
      print(message_batch)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Automatically fetches more pages as needed.
  for await (const messageBatch of client.messages.batches.list({
    limit: 20
  })) {
    console.log(messageBatch);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new BatchListParams
  {
      Limit = 20
  };

  // Automatically fetches more pages as needed
  var page = await client.Messages.Batches.List(parameters);
  await foreach (var messageBatch in page.Paginate())
  {
      Console.WriteLine(messageBatch);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  // Automatically fetches more pages as needed
  iter := client.Messages.Batches.ListAutoPaging(context.TODO(), anthropic.MessageBatchListParams{
  	Limit: anthropic.Int(20),
  })

  for iter.Next() {
  	messageBatch := iter.Current()
  	fmt.Println(messageBatch)
  }

  if err := iter.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Automatically fetches more pages as needed
  for (MessageBatch messageBatch : client
    .messages()
    .batches()
    .list(BatchListParams.builder().limit(20).build())
    .autoPager()) {
    System.out.println(messageBatch);
  }
  ```

  ```php PHP
  $client = new Client();

  // Automatically fetches more pages as needed
  foreach ($client->messages->batches->list(limit: 20)->pagingEachItem() as $messageBatch) {
      echo $messageBatch->id . "\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Automatically fetches more pages as needed
  client.messages.batches.list(limit: 20).auto_paging_each do |message_batch|
    puts message_batch
  end
  ```
</CodeGroup>

### Retrieving batch results

Once batch processing has ended, each Messages request in the batch has a result. There are four result types:

| Result type | Description                                                                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `succeeded` | Request was successful. Includes the message result.                                                                                                                        |
| `errored`   | Request encountered an error and a message was not created. Possible errors include invalid requests and internal server errors. You will not be billed for these requests. |
| `canceled`  | User canceled the batch before this request could be sent to the model. You will not be billed for these requests.                                                          |
| `expired`   | Batch reached its 24-hour expiration before this request could be sent to the model. You will not be billed for these requests.                                             |

The batch's `request_counts` shows an overview of your results, indicating how many requests reached each of these four states.

Results of the batch are available for download at the `results_url` property on the Message Batch, and if the organization permission allows, in the Console. Because of the potentially large size of the results, it's recommended to [stream results](https://platform.claude.com/docs/en/api/messages/batches/results) back rather than download them all at once.

<CodeGroup>
  ```bash cURL
  #!/bin/sh
  # Fetch the batch's results_url, then stream the .jsonl results it
  # points to. For per-result handling (retries, validation errors),
  # use the SDK examples in the other tabs.
  RESULTS_URL=$(curl -s "https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    | jq -r '.results_url')

  curl -s "$RESULTS_URL" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    | jq -r '"\(.result.type): \(.custom_id)"'
  ```

  ```bash CLI
  # Prints one line per result, e.g. `{"custom_id":"test-1","type":"succeeded",…}`.
  # For per-result handling (retries, validation errors), use the SDK
  # examples in the other tabs.
  ant messages:batches results \
    --message-batch-id msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d \
    --transform '{custom_id,"type":result.type,"error":result.error.error.type}' \
    --format jsonl
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Stream results file in memory-efficient chunks, processing one at a time
  for result in client.messages.batches.results(
      "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
  ):
      outcome = result.result
      match outcome.type:
          case "succeeded":
              print(f"Success! {result.custom_id}")
          case "errored":
              if outcome.error.error.type == "invalid_request_error":
                  # Request body must be fixed before re-sending request
                  print(f"Validation error {result.custom_id}")
              else:
                  # Request can be retried directly
                  print(f"Server error {result.custom_id}")
          case "expired":
              print(f"Request expired {result.custom_id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Stream results file in memory-efficient chunks, processing one at a time
  for await (const result of await client.messages.batches.results(
    "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"
  )) {
    switch (result.result.type) {
      case "succeeded":
        console.log(`Success! ${result.custom_id}`);
        break;
      case "errored":
        if (result.result.error.type === "invalid_request_error") {
          // Request body must be fixed before re-sending request
          console.log(`Validation error: ${result.custom_id}`);
        } else {
          // Request can be retried directly
          console.log(`Server error: ${result.custom_id}`);
        }
        break;
      case "expired":
        console.log(`Request expired: ${result.custom_id}`);
        break;
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  await foreach (var result in client.Messages.Batches.ResultsStreaming("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"))
  {
      switch (result.Result.Type)
      {
          case "succeeded":
              Console.WriteLine($"Success! {result.CustomID}");
              break;
          case "errored":
              if (result.Result.Error?.Type == "invalid_request")
              {
                  Console.WriteLine($"Validation error: {result.CustomID}");
              }
              else
              {
                  Console.WriteLine($"Server error: {result.CustomID}");
              }
              break;
          case "expired":
              Console.WriteLine($"Request expired: {result.CustomID}");
              break;
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.Batches.ResultsStreaming(context.TODO(), "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d", anthropic.MessageBatchResultsParams{})

  for stream.Next() {
  	result := stream.Current()

  	switch variant := result.Result.AsAny().(type) {
  	case anthropic.MessageBatchSucceededResult:
  		fmt.Printf("Success! %s\n", result.CustomID)
  	case anthropic.MessageBatchErroredResult:
  		fmt.Printf("Error: %s - %s\n", result.CustomID, variant.Error.Error.Message)
  	case anthropic.MessageBatchExpiredResult:
  		fmt.Printf("Request expired: %s\n", result.CustomID)
  	}
  }

  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.core.http.StreamResponse;
  import com.anthropic.models.messages.batches.BatchResultsParams;
  import com.anthropic.models.messages.batches.MessageBatchIndividualResponse;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Stream results file in memory-efficient chunks, processing one at a time
      try (
        StreamResponse<MessageBatchIndividualResponse> streamResponse = client
          .messages()
          .batches()
          .resultsStreaming(
            BatchResultsParams.builder()
              .messageBatchId("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d")
              .build()
          )
      ) {
        streamResponse
          .stream()
          .forEach(result -> {
            switch (result.result().type().value()) {
              case SUCCEEDED -> System.out.println("Success! " + result.customId());
              case ERRORED -> {
                if (result.result().asErrored().error().error().isInvalidRequestError()) {
                  // Request body must be fixed before re-sending request
                  System.out.println("Validation error: " + result.customId());
                } else {
                  // Request can be retried directly
                  System.out.println("Server error: " + result.customId());
                }
              }
              case EXPIRED -> System.out.println("Request expired: " + result.customId());
            }
          });
      }
  ```

  ```php PHP
  use Anthropic\Messages\Batches\MessageBatchErroredResult;
  use Anthropic\Messages\Batches\MessageBatchExpiredResult;
  use Anthropic\Messages\Batches\MessageBatchSucceededResult;

  $client = new Client();

  foreach ($client->messages->batches->resultsStream(messageBatchID: 'msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d') as $result) {
      switch (true) {
          case $result->result instanceof MessageBatchSucceededResult:
              echo "Success! {$result->customID}\n";
              break;
          case $result->result instanceof MessageBatchErroredResult:
              if ($result->result->error->error->type === "invalid_request_error") {
                  echo "Validation error: {$result->customID}\n";
              } else {
                  echo "Server error: {$result->customID}\n";
              }
              break;
          case $result->result instanceof MessageBatchExpiredResult:
              echo "Request expired: {$result->customID}\n";
              break;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  client.messages.batches.results_streaming("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d").each do |result|
    outcome = result.result
    case outcome
    when Anthropic::Models::Messages::MessageBatchSucceededResult
      puts "Success! #{result.custom_id}"
    when Anthropic::Models::Messages::MessageBatchErroredResult
      if outcome.error.type == :invalid_request
        puts "Validation error: #{result.custom_id}"
      else
        puts "Server error: #{result.custom_id}"
      end
    when Anthropic::Models::Messages::MessageBatchExpiredResult
      puts "Request expired: #{result.custom_id}"
    end
  end
  ```
</CodeGroup>

The results are in `.jsonl` format, where each line is a valid JSON object representing the result of a single request in the Message Batch. For each streamed result, you can do something different depending on its `custom_id` and result type. Here is an example set of results:

```jsonl .jsonl file
{"custom_id":"my-second-request","result":{"type":"succeeded","message":{"id":"msg_014VwiXbi91y3JMjcpyGBHX5","type":"message","role":"assistant","model":"claude-opus-5-5","content":[{"type":"text","text":"Hello again! It's nice to see you. How can I assist you today? Is there anything specific you'd like to chat about or any questions you have?"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":11,"output_tokens":36}}}}
{"custom_id":"my-first-request","result":{"type":"succeeded","message":{"id":"msg_01FqfsLoHwgeFbguDgpz48m7","type":"message","role":"assistant","model":"claude-opus-5-5","content":[{"type":"text","text":"Hello! How can I assist you today? Feel free to ask me any questions or let me know if there's anything you'd like to chat about."}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":10,"output_tokens":34}}}}
```

If your result has an error, its `result.error` will be set to the standard [error shape](https://platform.claude.com/docs/en/api/errors#error-shapes).

<Tip>
  **Batch results may not match input order**

  Batch results can be returned in any order, and may not match the ordering of requests when the batch was created. In the preceding example, the result for the second batch request is returned before the first. To correctly match results with their corresponding requests, always use the `custom_id` field.
</Tip>

### Canceling a Message Batch

You can cancel a Message Batch that is currently processing using the [cancel endpoint](https://platform.claude.com/docs/en/api/messages/batches/cancel). Immediately after cancellation, a batch's `processing_status` will be `canceling`. You can use the same polling technique described earlier to wait until cancellation is finalized. Canceled batches end up with a status of `ended` and may contain partial results for requests that were processed before cancellation.

<CodeGroup>
  ```bash cURL
  #!/bin/sh
  # ...
  curl --request POST https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID/cancel \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  #!/bin/bash
  # ...
  ant messages:batches cancel --message-batch-id "$MESSAGE_BATCH_ID"
  ```

  ```python Python
  client = anthropic.Anthropic()

  MESSAGE_BATCH_ID = "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d"

  message_batch = client.messages.batches.cancel(
      MESSAGE_BATCH_ID,
  )
  print(message_batch)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const messageBatch = await client.messages.batches.cancel(MESSAGE_BATCH_ID);
  console.log(messageBatch);
  ```

  ```csharp C#
  AnthropicClient client = new();
  string messageBatchId = Environment.GetEnvironmentVariable("MESSAGE_BATCH_ID");

  var messageBatch = await client.Messages.Batches.Cancel(messageBatchId);
  Console.WriteLine(messageBatch);
  ```

  ```go Go
  client := anthropic.NewClient()
  messageBatchID := os.Getenv("MESSAGE_BATCH_ID")

  messageBatch, err := client.Messages.Batches.Cancel(context.TODO(), messageBatchID, anthropic.MessageBatchCancelParams{})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(messageBatch)
  ```

  ```java Java
  import com.anthropic.models.messages.batches.*;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageBatch messageBatch = client
        .messages()
        .batches()
        .cancel("msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d");
      System.out.println(messageBatch);
  ```

  ```php PHP
  $client = new Client();

  $messageBatch = $client->messages->batches->cancel(
      messageBatchID: 'msgbatch_example_id',
  );
  echo $messageBatch;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message_batch_id = ENV.fetch("MESSAGE_BATCH_ID")
  message_batch = client.messages.batches.cancel(message_batch_id)
  puts message_batch
  ```
</CodeGroup>

The response shows the batch in a `canceling` state:

```json Output
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch",
  "processing_status": "canceling",
  "request_counts": {
    "processing": 2,
    "succeeded": 0,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "ended_at": null,
  "created_at": "2024-09-24T18:37:24.100435Z",
  "expires_at": "2024-09-25T18:37:24.100435Z",
  "cancel_initiated_at": "2024-09-24T18:39:03.114875Z",
  "results_url": null
}
```

### Using prompt caching with Message Batches

The Message Batches API supports prompt caching, allowing you to potentially reduce costs and processing time for batch requests. The pricing discounts from prompt caching and Message Batches can stack, providing even greater cost savings when both features are used together. However, because batch requests are processed asynchronously and concurrently, cache hits are provided on a best-effort basis. Users typically experience cache hit rates ranging from 30% to 98%, depending on their traffic patterns.

To maximize the likelihood of cache hits in your batch requests:

1. Include identical `cache_control` blocks in every Message request within your batch.
2. Maintain a steady stream of requests to prevent cache entries from expiring after their 5-minute lifetime.
3. Structure your requests to share as much cached content as possible.

Example of implementing prompt caching in a batch:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/batches \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data \
  '{
      "requests": [
          {
              "custom_id": "my-first-request",
              "params": {
                  "model": "claude-opus-5-5",
                  "max_tokens": 1024,
                  "system": [
                      {
                          "type": "text",
                          "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                      },
                      {
                          "type": "text",
                          "text": "<the entire contents of Pride and Prejudice>",
                          "cache_control": {"type": "ephemeral"}
                      }
                  ],
                  "messages": [
                      {"role": "user", "content": "Analyze the major themes in Pride and Prejudice."}
                  ]
              }
          },
          {
              "custom_id": "my-second-request",
              "params": {
                  "model": "claude-opus-5-5",
                  "max_tokens": 1024,
                  "system": [
                      {
                          "type": "text",
                          "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                      },
                      {
                          "type": "text",
                          "text": "<the entire contents of Pride and Prejudice>",
                          "cache_control": {"type": "ephemeral"}
                      }
                  ],
                  "messages": [
                      {"role": "user", "content": "Write a summary of Pride and Prejudice."}
                  ]
              }
          }
      ]
  }'
  ```

  ```bash CLI
  ant messages:batches create <<'YAML'
  requests:
    - custom_id: my-first-request
      params:
        model: claude-opus-5-5
        max_tokens: 1024
        system:
          - type: text
            text: >
              You are an AI assistant tasked with analyzing literary works. Your
              goal is to provide insightful commentary on themes, characters, and
              writing style.
          - type: text
            text: "<the entire contents of Pride and Prejudice>"
            cache_control:
              type: ephemeral
        messages:
          - role: user
            content: Analyze the major themes in Pride and Prejudice.
    - custom_id: my-second-request
      params:
        model: claude-opus-5-5
        max_tokens: 1024
        system:
          - type: text
            text: >
              You are an AI assistant tasked with analyzing literary works. Your
              goal is to provide insightful commentary on themes, characters, and
              writing style.
          - type: text
            text: "<the entire contents of Pride and Prejudice>"
            cache_control:
              type: ephemeral
        messages:
          - role: user
            content: Write a summary of Pride and Prejudice.
  YAML
  ```

  ```python Python
  from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
  from anthropic.types.messages.batch_create_params import Request

  client = anthropic.Anthropic()

  message_batch = client.messages.batches.create(
      requests=[
          Request(
              custom_id="my-first-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-opus-5-5",
                  max_tokens=1024,
                  system=[
                      {
                          "type": "text",
                          "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
                      },
                      {
                          "type": "text",
                          "text": "<the entire contents of Pride and Prejudice>",
                          "cache_control": {"type": "ephemeral"},
                      },
                  ],
                  messages=[
                      {
                          "role": "user",
                          "content": "Analyze the major themes in Pride and Prejudice.",
                      }
                  ],
              ),
          ),
          Request(
              custom_id="my-second-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-opus-5-5",
                  max_tokens=1024,
                  system=[
                      {
                          "type": "text",
                          "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
                      },
                      {
                          "type": "text",
                          "text": "<the entire contents of Pride and Prejudice>",
                          "cache_control": {"type": "ephemeral"},
                      },
                  ],
                  messages=[
                      {
                          "role": "user",
                          "content": "Write a summary of Pride and Prejudice.",
                      }
                  ],
              ),
          ),
      ]
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const messageBatch = await client.messages.batches.create({
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          system: [
            {
              type: "text",
              text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
            },
            {
              type: "text",
              text: "<the entire contents of Pride and Prejudice>",
              cache_control: { type: "ephemeral" }
            }
          ],
          messages: [
            { role: "user", content: "Analyze the major themes in Pride and Prejudice." }
          ]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          system: [
            {
              type: "text",
              text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
            },
            {
              type: "text",
              text: "<the entire contents of Pride and Prejudice>",
              cache_control: { type: "ephemeral" }
            }
          ],
          messages: [{ role: "user", content: "Write a summary of Pride and Prejudice." }]
        }
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;
  using Anthropic.Models.Messages.Batches;

  AnthropicClient client = new()
  {
      ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
  };

  var messageBatch = await client.Messages.Batches.Create(new BatchCreateParams
  {
      Requests =
      [
          new()
          {
              CustomID = "my-first-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus5_5,
                  MaxTokens = 1024,
                  System = new List<TextBlockParam>
                  {
                      new()
                      {
                          Text = "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                      },
                      new()
                      {
                          Text = "<the entire contents of Pride and Prejudice>",
                          CacheControl = new()
                      }
                  },
                  Messages =
                  [
                      new() { Role = Role.User, Content = "Analyze the major themes in Pride and Prejudice." }
                  ]
              }
          },
          new()
          {
              CustomID = "my-second-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus5_5,
                  MaxTokens = 1024,
                  System = new List<TextBlockParam>
                  {
                      new()
                      {
                          Text = "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                      },
                      new()
                      {
                          Text = "<the entire contents of Pride and Prejudice>",
                          CacheControl = new()
                      }
                  },
                  Messages =
                  [
                      new() { Role = Role.User, Content = "Write a summary of Pride and Prejudice." }
                  ]
              }
          }
      ]
  });
  ```

  ```go Go
  client := anthropic.NewClient()

  messageBatch, err := client.Messages.Batches.New(context.TODO(), anthropic.MessageBatchNewParams{
  	Requests: []anthropic.MessageBatchNewParamsRequest{
  		{
  			CustomID: "my-first-request",
  			Params: anthropic.MessageBatchNewParamsRequestParams{
  				Model:     anthropic.ModelClaudeOpus5_5,
  				MaxTokens: 1024,
  				System: []anthropic.TextBlockParam{
  					{
  						Text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
  					},
  					{
  						Text:         "<the entire contents of Pride and Prejudice>",
  						CacheControl: anthropic.NewCacheControlEphemeralParam(),
  					},
  				},
  				Messages: []anthropic.MessageParam{
  					anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the major themes in Pride and Prejudice.")),
  				},
  			},
  		},
  		{
  			CustomID: "my-second-request",
  			Params: anthropic.MessageBatchNewParamsRequestParams{
  				Model:     anthropic.ModelClaudeOpus5_5,
  				MaxTokens: 1024,
  				System: []anthropic.TextBlockParam{
  					{
  						Text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
  					},
  					{
  						Text:         "<the entire contents of Pride and Prejudice>",
  						CacheControl: anthropic.NewCacheControlEphemeralParam(),
  					},
  				},
  				Messages: []anthropic.MessageParam{
  					anthropic.NewUserMessage(anthropic.NewTextBlock("Write a summary of Pride and Prejudice.")),
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(messageBatch)
  ```

  ```java Java
  import com.anthropic.models.messages.CacheControlEphemeral;
  // ...
  import com.anthropic.models.messages.batches.*;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BatchCreateParams createParams = BatchCreateParams.builder()
        .addRequest(
          BatchCreateParams.Request.builder()
            .customId("my-first-request")
            .params(
              BatchCreateParams.Request.Params.builder()
                .model(Model.CLAUDE_OPUS_5_5)
                .maxTokens(1024)
                .systemOfTextBlockParams(
                  List.of(
                    TextBlockParam.builder()
                      .text(
                        "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                      )
                      .build(),
                    TextBlockParam.builder()
                      .text("<the entire contents of Pride and Prejudice>")
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()
                  )
                )
                .addUserMessage("Analyze the major themes in Pride and Prejudice.")
                .build()
            )
            .build()
        )
        .addRequest(
          BatchCreateParams.Request.builder()
            .customId("my-second-request")
            .params(
              BatchCreateParams.Request.Params.builder()
                .model(Model.CLAUDE_OPUS_5_5)
                .maxTokens(1024)
                .systemOfTextBlockParams(
                  List.of(
                    TextBlockParam.builder()
                      .text(
                        "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
                      )
                      .build(),
                    TextBlockParam.builder()
                      .text("<the entire contents of Pride and Prejudice>")
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()
                  )
                )
                .addUserMessage("Write a summary of Pride and Prejudice.")
                .build()
            )
            .build()
        )
        .build();

      MessageBatch messageBatch = client.messages().batches().create(createParams);
  ```

  ```php PHP
  $client = new Client();

  $messageBatch = $client->messages->batches->create(
      requests: [
          [
              'custom_id' => 'my-first-request',
              'params' => [
                  'model' => 'claude-opus-5-5',
                  'max_tokens' => 1024,
                  'system' => [
                      [
                          'type' => 'text',
                          'text' => 'You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n'
                      ],
                      [
                          'type' => 'text',
                          'text' => '<the entire contents of Pride and Prejudice>',
                          'cache_control' => ['type' => 'ephemeral']
                      ]
                  ],
                  'messages' => [
                      ['role' => 'user', 'content' => 'Analyze the major themes in Pride and Prejudice.']
                  ]
              ]
          ],
          [
              'custom_id' => 'my-second-request',
              'params' => [
                  'model' => 'claude-opus-5-5',
                  'max_tokens' => 1024,
                  'system' => [
                      [
                          'type' => 'text',
                          'text' => 'You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n'
                      ],
                      [
                          'type' => 'text',
                          'text' => '<the entire contents of Pride and Prejudice>',
                          'cache_control' => ['type' => 'ephemeral']
                      ]
                  ],
                  'messages' => [
                      ['role' => 'user', 'content' => 'Write a summary of Pride and Prejudice.']
                  ]
              ]
          ]
      ],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message_batch = client.messages.batches.create(
    requests: [
      {
        custom_id: "my-first-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          system: [
            {
              type: "text",
              text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
            },
            {
              type: "text",
              text: "<the entire contents of Pride and Prejudice>",
              cache_control: { type: "ephemeral" }
            }
          ],
          messages: [
            { role: "user", content: "Analyze the major themes in Pride and Prejudice." }
          ]
        }
      },
      {
        custom_id: "my-second-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 1024,
          system: [
            {
              type: "text",
              text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
            },
            {
              type: "text",
              text: "<the entire contents of Pride and Prejudice>",
              cache_control: { type: "ephemeral" }
            }
          ],
          messages: [
            { role: "user", content: "Write a summary of Pride and Prejudice." }
          ]
        }
      }
    ]
  )
  ```
</CodeGroup>

In this example, both requests in the batch include identical system messages and the full text of Pride and Prejudice marked with `cache_control` to increase the likelihood of cache hits.

### Server tools and the agentic loop

All [server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools) (web search, web fetch, code execution, MCP connectors, advisor, and tool search) work in batch requests. The batch worker runs the same server-side agentic loop as the synchronous Messages API.

Because there is no open connection to maintain, the batch loop runs **more iterations per turn** than a synchronous request before it returns `stop_reason: "pause_turn"`. If a batch result comes back with `pause_turn`, the turn did not finish; you can continue it by submitting the paused assistant content in a follow-up request (batch or synchronous) exactly as shown in the [pause\_turn continuation pattern](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn).

The batch worker additionally throttles `web_search` per organization so that highly concurrent batch processing does not exhaust your organization's web-search rate limit. The batch retries throttled requests automatically; you don't need to handle this yourself, but very large web-search batches might take longer to complete.

### Extended output (beta)

The `output-300k-2026-03-24` beta header raises the `max_tokens` cap to 300,000 for batch requests using Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, or Claude Haiku 5.5. Include the header to generate outputs far longer than the standard 128k `max_tokens` limit in a single turn.

<Note>
  Extended output is available on the Message Batches API only, not the synchronous Messages API. It is supported on the Claude API and Claude Platform on AWS, and is not currently available on Amazon Bedrock, Google Cloud, or Microsoft Foundry.
</Note>

Use extended output for long-form generation such as book-length drafts and technical documentation, exhaustive structured data extraction, large code-generation scaffolds, and long reasoning chains.

A single 300k-token generation can take over an hour to complete, so plan your batch submissions with the 24-hour processing window in mind. Standard batch pricing (50% of standard API prices) applies.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/batches \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "anthropic-beta: output-300k-2026-03-24" \
       --header "content-type: application/json" \
       --data \
  '{
      "requests": [
          {
              "custom_id": "long-form-request",
              "params": {
                  "model": "claude-opus-5-5",
                  "max_tokens": 300000,
                  "messages": [
                      {"role": "user", "content": "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices."}
                  ]
              }
          }
      ]
  }'
  ```

  ```bash CLI
  ant beta:messages:batches create --beta output-300k-2026-03-24 <<'YAML'
  requests:
    - custom_id: long-form-request
      params:
        model: claude-opus-5-5
        max_tokens: 300000
        messages:
          - role: user
            content: >-
              Write a comprehensive technical guide to building distributed
              systems, covering architecture patterns, consistency models,
              fault tolerance, and operational best practices.
  YAML
  ```

  ```python Python
  from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
  from anthropic.types.beta.messages.batch_create_params import Request

  client = anthropic.Anthropic()

  message_batch = client.beta.messages.batches.create(
      betas=["output-300k-2026-03-24"],
      requests=[
          Request(
              custom_id="long-form-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-opus-5-5",
                  max_tokens=300_000,
                  messages=[
                      {
                          "role": "user",
                          "content": "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices.",
                      }
                  ],
              ),
          ),
      ],
  )

  print(message_batch)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const messageBatch = await client.beta.messages.batches.create({
    betas: ["output-300k-2026-03-24"],
    requests: [
      {
        custom_id: "long-form-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 300000,
          messages: [
            {
              role: "user",
              content:
                "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices."
            }
          ]
        }
      }
    ]
  });

  console.log(messageBatch);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta.Messages;
  using Anthropic.Models.Beta.Messages.Batches;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  var batch = await client.Beta.Messages.Batches.Create(new BatchCreateParams
  {
      Betas = ["output-300k-2026-03-24"],
      Requests =
      [
          new()
          {
              CustomID = "long-form-request",
              Params = new()
              {
                  Model = Model.ClaudeOpus5_5,
                  MaxTokens = 300_000,
                  Messages =
                  [
                      new() { Role = Role.User, Content = "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices." }
                  ]
              }
          }
      ]
  });

  Console.WriteLine(batch);
  ```

  ```go Go
  client := anthropic.NewClient()

  batch, err := client.Beta.Messages.Batches.New(context.Background(),
  	anthropic.BetaMessageBatchNewParams{
  		Betas: []anthropic.AnthropicBeta{"output-300k-2026-03-24"},
  		Requests: []anthropic.BetaMessageBatchNewParamsRequest{
  			{
  				CustomID: "long-form-request",
  				Params: anthropic.BetaMessageBatchNewParamsRequestParams{
  					Model:     anthropic.ModelClaudeOpus5_5,
  					MaxTokens: 300_000,
  					Messages: []anthropic.BetaMessageParam{
  						anthropic.NewBetaUserMessage(
  							anthropic.NewBetaTextBlock("Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices."),
  						),
  					},
  				},
  			},
  		},
  	})
  if err != nil {
  	panic(err)
  }

  fmt.Println(batch.ID)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.batches.*;

  void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    BatchCreateParams params = BatchCreateParams.builder()
      .addBeta("output-300k-2026-03-24")
      .addRequest(
        BatchCreateParams.Request.builder()
          .customId("long-form-request")
          .params(
            BatchCreateParams.Request.Params.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(300_000L)
              .addUserMessage("Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices.")
              .build()
          )
          .build()
      )
      .build();

    BetaMessageBatch messageBatch = client.beta().messages().batches().create(params);

    IO.println(messageBatch);
  }
  ```

  ```php PHP
  $client = new Client();

  $batch = $client->beta->messages->batches->create(
      betas: ['output-300k-2026-03-24'],
      requests: [
          [
              'custom_id' => 'long-form-request',
              'params' => [
                  'model' => 'claude-opus-5-5',
                  'max_tokens' => 300_000,
                  'messages' => [
                      ['role' => 'user', 'content' => 'Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices.']
                  ]
              ]
          ]
      ],
  );

  echo $batch->id;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  batch = client.beta.messages.batches.create(
    betas: ["output-300k-2026-03-24"],
    requests: [
      {
        custom_id: "long-form-request",
        params: {
          model: "claude-opus-5-5",
          max_tokens: 300_000,
          messages: [
            { role: "user", content: "Write a comprehensive technical guide to building distributed systems, covering architecture patterns, consistency models, fault tolerance, and operational best practices." }
          ]
        }
      }
    ]
  )

  puts batch
  ```
</CodeGroup>

### Best practices for effective batching

To get the most out of the Batches API:

* Monitor batch processing status regularly and implement appropriate retry logic for failed requests.
* Use meaningful `custom_id` values to easily match results with requests, since order is not guaranteed.
* Consider breaking very large datasets into multiple batches for better manageability.
* Dry run a single request shape with the Messages API to avoid validation errors.

### Troubleshooting common issues

If experiencing unexpected behavior:

* Verify that the total batch request size doesn't exceed 256 MB. If the request size is too large, you may get a 413 `request_too_large` error.
* Check that you're using [supported models](https://platform.claude.com/docs/en/build-with-claude/batch-processing#supported-models) for all requests in the batch.
* Ensure each request in the batch has a unique `custom_id`.
* Ensure that it has been less than 29 days since batch `created_at` (not processing `ended_at`) time. If over 29 days have passed, results will no longer be viewable.
* Confirm that the batch has not been canceled.

Note that the failure of one request in a batch does not affect the processing of other requests.

## Batch storage and privacy

* **Workspace isolation**: Batches are isolated within the Workspace they are created in. They can only be accessed by API requests in that same Workspace, or users with permission to view Workspace batches in the Console.

* **Result availability**: Batch results are available for 29 days after the batch is created, allowing ample time for retrieval and processing.

## Data retention

Batch processing stores request and response data for up to 29 days after batch creation. You can delete a message batch at any time after processing using the `DELETE /v1/messages/batches/{batch_id}` endpoint. To delete an in-progress batch, cancel it first. Asynchronous processing requires server-side storage of both inputs and outputs until batch completion and result retrieval.

For ZDR eligibility across all features, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).

## FAQ

<AccordionGroup>
  <Accordion title="How long does it take for a batch to process?">
    Batches may take up to 24 hours for processing, but many finish sooner. Actual processing time depends on the size of the batch, current demand, and your request volume. It is possible for a batch to expire and not complete within 24 hours.
  </Accordion>

  <Accordion title="Is the Batches API available for all models?">
    See [Supported models](https://platform.claude.com/docs/en/build-with-claude/batch-processing#supported-models) for the list of supported models.
  </Accordion>

  <Accordion title="Can I use the Message Batches API with other API features?">
    Yes, the Message Batches API supports nearly all features available in the Messages API, including most beta features. A small number of parameters (`stream`, `speed`, and `max_tokens: 0`) are not supported. See [What can be batched](https://platform.claude.com/docs/en/build-with-claude/batch-processing#what-can-be-batched) for the full list.
  </Accordion>

  <Accordion title="How does the Message Batches API affect pricing?">
    The Message Batches API offers a 50% discount on all usage compared to standard API prices. This applies to input tokens, output tokens, and any special tokens. For more on pricing, visit [Pricing](https://claude.com/pricing#anthropic-api).
  </Accordion>

  <Accordion title="Can I update a batch after it's been submitted?">
    No, once a batch has been submitted, it cannot be modified. If you need to make changes, you should cancel the current batch and submit a new one. Note that cancellation may not take immediate effect.
  </Accordion>

  <Accordion title="Are there Message Batches API rate limits and do they interact with the Messages API rate limits?">
    The Message Batches API has HTTP requests-based rate limits in addition to limits on the number of requests in need of processing. See [Message Batches API rate limits](https://platform.claude.com/docs/en/api/rate-limits#message-batches-api). Usage of the Batches API does not affect rate limits in the Messages API.
  </Accordion>

  <Accordion title="How do I handle errors in my batch requests?">
    When you retrieve the results, each request has a `result` field indicating whether it `succeeded`, `errored`, was `canceled`, or `expired`. For `errored` results, additional error information is provided. View the error response object in the [API reference](https://platform.claude.com/docs/en/api/messages/batches/create).
  </Accordion>

  <Accordion title="How does the Message Batches API handle privacy and data separation?">
    The Message Batches API is designed with strong privacy and data separation measures:

    1. Batches and their results are isolated within the Workspace in which they were created. This means they can only be accessed by API requests in that same Workspace.
    2. Each request within a batch is processed independently, with no data leakage between requests.
    3. Results are only available for a limited time (29 days), and follow Anthropic's [data retention policy](https://support.claude.com/en/articles/7996866-how-long-do-you-store-personal-data).
    4. Downloading batch results in the Console can be disabled on the organization-level or on a per-workspace basis.
  </Accordion>

  <Accordion title="Can I use prompt caching in the Message Batches API?">
    Yes, it is possible to use prompt caching with Message Batches API. However, because asynchronous batch requests can be processed concurrently and in any order, cache hits are provided on a best-effort basis.
  </Accordion>
</AccordionGroup>

## Next steps

<CardGroup cols={2}>
  <Card title="Search results" icon="magnifying-glass" href="https://platform.claude.com/docs/en/build-with-claude/search-results">
    Enable natural citations for RAG applications by providing search results with source attribution.
  </Card>

  <Card title="Prompt caching" icon="database" href="https://platform.claude.com/docs/en/build-with-claude/prompt-caching">
    Reduce cost and latency by caching prompt prefixes shared across requests in a batch.
  </Card>
</CardGroup>

---
title: Define tools
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
description: Specify tool schemas, write effective descriptions, and control when Claude calls your tools.
---

## Prerequisites

* Familiarity with the [tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
* A Claude API key and a working SDK or cURL setup

<Tip>
  If using Claude with tool use and thinking, see [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) for more information.
</Tip>

## Specifying client tools

Client tools are specified in the `tools` top-level parameter of the API request. Anthropic-schema client tools, such as the bash and text editor tools, are declared by a date-versioned `type`; see each tool's page, linked from the [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference), for the fields it accepts. The computer use and browser use tools are [client toolsets](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference#client-toolsets): a single entry with no `name` that declares a fixed set of member tools. A user-defined tool definition includes:

| Parameter        | Description                                                                                                                                                                                                                            |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`           | The name of the tool. Must match the regex `^[a-zA-Z0-9_-]{1,128}$`.                                                                                                                                                                   |
| `description`    | A detailed plaintext description of what the tool does, when it should be used, and how it behaves.                                                                                                                                    |
| `input_schema`   | A [JSON Schema](https://json-schema.org/) object defining the expected parameters for the tool.                                                                                                                                        |
| `input_examples` | (Optional) An array of example input objects to help Claude understand how to use the tool. See [Providing tool use examples](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#providing-tool-use-examples). |

For the full set of optional properties available on any single tool definition, including `cache_control`, `strict`, `defer_loading`, and `allowed_callers`, see the [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference#tool-definition-properties). A client toolset entry accepts `cache_control` and `allowed_callers` on the entry and sets `defer_loading` per member; see [Client toolsets](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference#client-toolsets).

<Accordion title="Example simple tool definition">
  ```json JSON
  {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
        }
      },
      "required": ["location"]
    }
  }
  ```

  This tool, named `get_weather`, expects an input object with a required `location` string and an optional `unit` string that must be either "celsius" or "fahrenheit".
</Accordion>

### Tool use system prompt

When you call the Claude API with the `tools` parameter, the API constructs a special system prompt from the tool definitions, tool configuration, and any user-specified system prompt. The constructed prompt is designed to instruct the model to use the specified tool(s) and provide the necessary context for the tool to operate properly:

```text wrap
In this environment you have access to a set of tools you can use to answer the user's question.
{{ FORMATTING INSTRUCTIONS }}
String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.
Here are the functions available in JSONSchema format:
{{ TOOL DEFINITIONS IN JSON SCHEMA }}
{{ USER SYSTEM PROMPT }}
{{ TOOL CONFIGURATION }}
```

### Best practices for tool definitions

To get the best performance out of Claude when using tools, follow these guidelines:

* **Provide extremely detailed descriptions.** This is by far the most important factor in tool performance. Your descriptions should explain every detail about the tool, including:

  * What the tool does
  * When it should be used (and when it shouldn't)
  * What each parameter means and how it affects the tool's behavior
  * Any important caveats or limitations, such as what information the tool does not return if the tool name is unclear. The more context you can give Claude about your tools, the better it will be at determining when and how to use them. Aim for at least 3–4 sentences for each tool description, more if the tool is complex.

* **Prioritize descriptions, but consider using `input_examples` for complex tools.** Clear descriptions are most important, but for tools with complex inputs, nested objects, or format-sensitive parameters, you can use the `input_examples` field to provide schema-validated examples. See [Providing tool use examples](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#providing-tool-use-examples) for details.

* **Consolidate related operations into fewer tools.** Rather than creating a separate tool for every action (`create_pr`, `review_pr`, `merge_pr`), group them into a single tool with an `action` parameter. Fewer, more capable tools reduce selection ambiguity and make your tool surface easier for Claude to navigate.

* **Use meaningful namespacing in tool names.** When your tools span multiple services or resources, prefix names with the service (for example, `github_list_prs`, `slack_send_message`). This makes tool selection unambiguous as your library grows, and is especially important when using [tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).

* **Design tool responses to return only high-signal information.** Return semantic, stable identifiers (for example, slugs or UUIDs) rather than opaque internal references, and include only the fields Claude needs to reason about its next step. Bloated responses waste context and make it harder for Claude to extract what matters.

* **Ask for an explanation, not reasoning.** If a parameter asks Claude why it is making the call, ask for a short explanation or the supporting evidence. A parameter that asks for the model's thinking or step-by-step reasoning may lead to a `reasoning_extraction` refusal. See [Keep reasoning in thinking blocks](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks).

<AccordionGroup>
  <Accordion title="Example of a good tool description">
    ```json JSON
    {
      "name": "get_stock_price",
      "description": "Retrieves the current stock price for a given ticker symbol. The ticker symbol must be a valid symbol for a publicly traded company on a major US stock exchange like NYSE or NASDAQ. The tool will return the latest trade price in USD. It should be used when the user asks about the current or most recent price of a specific stock. It will not provide any other information about the stock or company.",
      "input_schema": {
        "type": "object",
        "properties": {
          "ticker": {
            "type": "string",
            "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
          }
        },
        "required": ["ticker"]
      }
    }
    ```
  </Accordion>

  <Accordion title="Example poor tool description">
    ```json JSON
    {
      "name": "get_stock_price",
      "description": "Gets the stock price for a ticker.",
      "input_schema": {
        "type": "object",
        "properties": {
          "ticker": {
            "type": "string"
          }
        },
        "required": ["ticker"]
      }
    }
    ```
  </Accordion>
</AccordionGroup>

The good description clearly explains what the tool does, when to use it, what data it returns, and what the `ticker` parameter means. The poor description is too brief and leaves Claude with many open questions about the tool's behavior and usage.

<Tip>
  For deeper guidance on tool design (consolidation, naming, and response shaping), see [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents).
</Tip>

## Providing tool use examples

You can provide concrete examples of valid tool inputs to help Claude understand how to use your tools more effectively. This is particularly useful for complex tools with nested objects, optional parameters, or format-sensitive inputs.

### Basic usage

Add an optional `input_examples` field to your tool definition with an array of example input objects. Each example must be valid according to the tool's `input_schema`:

<CodeGroup>
  ```bash cURL
  curl -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @- <<'EOF'
  {
    "model": "claude-opus-5-5",
    "max_tokens": 1024,
    "tools": [
      {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"],
              "description": "The unit of temperature"
            }
          },
          "required": ["location"]
        },
        "input_examples": [
          {"location": "San Francisco, CA", "unit": "fahrenheit"},
          {"location": "Tokyo, Japan", "unit": "celsius"},
          {"location": "New York, NY"}
        ]
      }
    ],
    "messages": [
      {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]
  }
  EOF
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
          unit:
            type: string
            enum: [celsius, fahrenheit]
            description: The unit of temperature
        required: [location]
      input_examples:
        - location: San Francisco, CA
          unit: fahrenheit
        - location: Tokyo, Japan
          unit: celsius
        - location: New York, NY  # 'unit' is optional
  messages:
    - role: user
      content: What's the weather like in San Francisco?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA",
                      },
                      "unit": {
                          "type": "string",
                          "enum": ["celsius", "fahrenheit"],
                          "description": "The unit of temperature",
                      },
                  },
                  "required": ["location"],
              },
              "input_examples": [
                  {"location": "San Francisco, CA", "unit": "fahrenheit"},
                  {"location": "Tokyo, Japan", "unit": "celsius"},
                  {
                      "location": "New York, NY"  # 'unit' is optional
                  },
              ],
          }
      ],
      messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"],
              description: "The unit of temperature"
            }
          },
          required: ["location"]
        },
        input_examples: [
          {
            location: "San Francisco, CA",
            unit: "fahrenheit"
          },
          {
            location: "Tokyo, Japan",
            unit: "celsius"
          },
          {
            location: "New York, NY"
            // Demonstrates that 'unit' is optional
          }
        ]
      }
    ],
    messages: [{ role: "user", content: "What's the weather like in San Francisco?" }]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Tools = [
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the current weather in a given location",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                      ["unit"] = JsonSerializer.SerializeToElement(new { type = "string", @enum = new[] { "celsius", "fahrenheit" }, description = "The unit of temperature" }),
                  },
                  Required = ["location"],
              },
              InputExamples =
              [
                  new Dictionary<string, JsonElement>()
                  {
                      { "location", JsonSerializer.SerializeToElement("San Francisco, CA") },
                      { "unit", JsonSerializer.SerializeToElement("fahrenheit") },
                  },
                  new Dictionary<string, JsonElement>()
                  {
                      { "location", JsonSerializer.SerializeToElement("Tokyo, Japan") },
                      { "unit", JsonSerializer.SerializeToElement("celsius") },
                  },
                  new Dictionary<string, JsonElement>()
                  {
                      { "location", JsonSerializer.SerializeToElement("New York, NY") },
                  },
              ],
          }),
      ],
      Messages = [
          new() { Role = Role.User, Content = "What's the weather like in San Francisco?" }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  					"unit": map[string]any{
  						"type":        "string",
  						"enum":        []string{"celsius", "fahrenheit"},
  						"description": "The unit of temperature",
  					},
  				},
  				Required: []string{"location"},
  			},
  			InputExamples: []map[string]any{
  				{
  					"location": "San Francisco, CA",
  					"unit":     "fahrenheit",
  				},
  				{
  					"location": "Tokyo, Japan",
  					"unit":     "celsius",
  				},
  				{
  					"location": "New York, NY",
  					// Demonstrates that 'unit' is optional
  				},
  			},
  		}},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather like in San Francisco?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addTool(Tool.builder()
              .name("get_weather")
              .description("Get the current weather in a given location")
              .inputSchema(InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "location", Map.of(
                          "type", "string",
                          "description", "The city and state, e.g. San Francisco, CA"
                      ),
                      "unit", Map.of(
                          "type", "string",
                          "enum", List.of("celsius", "fahrenheit"),
                          "description", "The unit of temperature"
                      )
                  )))
                  .required(List.of("location"))
                  .build())
              .putAdditionalProperty("input_examples", JsonValue.from(List.of(
                  Map.of(
                      "location", "San Francisco, CA",
                      "unit", "fahrenheit"
                  ),
                  Map.of(
                      "location", "Tokyo, Japan",
                      "unit", "celsius"
                  ),
                  Map.of(
                      "location", "New York, NY"
                  )
              )))
              .build())
          .addUserMessage("What's the weather like in San Francisco?")
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather like in San Francisco?"]
      ],
      model: 'claude-opus-5-5',
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ],
                      'unit' => [
                          'type' => 'string',
                          'enum' => ['celsius', 'fahrenheit'],
                          'description' => 'The unit of temperature'
                      ]
                  ],
                  'required' => ['location']
              ],
              'input_examples' => [
                  [
                      'location' => 'San Francisco, CA',
                      'unit' => 'fahrenheit'
                  ],
                  [
                      'location' => 'Tokyo, Japan',
                      'unit' => 'celsius'
                  ],
                  [
                      'location' => 'New York, NY'
                  ]
              ]
          ]
      ],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            },
            unit: {
              type: "string",
              enum: ["celsius", "fahrenheit"],
              description: "The unit of temperature"
            }
          },
          required: ["location"]
        },
        input_examples: [
          {
            location: "San Francisco, CA",
            unit: "fahrenheit"
          },
          {
            location: "Tokyo, Japan",
            unit: "celsius"
          },
          {
            location: "New York, NY"
          }
        ]
      }
    ],
    messages: [
      { role: "user", content: "What's the weather like in San Francisco?" }
    ]
  )
  puts message
  ```
</CodeGroup>

Examples are included in the prompt alongside your tool schema, showing Claude concrete patterns for well-formed tool calls. This helps Claude understand when to include optional parameters, what formats to use, and how to structure complex inputs.

### Requirements and limitations

* **Schema validation** - Each example must be valid according to the tool's `input_schema`. Invalid examples return a 400 error
* **Not supported for server-side tools or client toolsets** - Input examples work on user-defined and Anthropic-schema client tools other than the [computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) and [browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) toolsets, but not on server tools such as web search or code execution
* **Token cost** - Examples add to prompt tokens: \~20–50 tokens for simple examples, \~100–200 tokens for complex nested objects

## Controlling Claude's output

### Forcing tool use

In some cases, you may want Claude to use a specific tool to answer the user's question, even if Claude would otherwise answer directly without calling a tool. You can do this by specifying the tool in the `tool_choice` field of the request.

Not every model and setting supports forced tool use. Where it isn't supported, `tool_choice: {"type": "any"}` and `tool_choice: {"type": "tool", "name": "..."}` fail, while `tool_choice: {"type": "auto"}` (the default) and `tool_choice: {"type": "none"}` still work:

| Model or setting                                                                                                                              | Restriction                                                                                                         | What to use instead                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manual [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) (`thinking: {type: "enabled"}`)           | `any` and `tool` are not supported and result in an error                                                           | `auto` or `none`. [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) itself doesn't block forced tool use (Claude Opus 5 and Claude Haiku 5.5 support it with thinking on); the models in the next row reject forced tool use regardless of thinking settings                                                                                     |
| Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and [Claude Mythos 5.1](https://platform.claude.com/docs/en/models/mythos-5-1/overview) | `any` and `tool` return a [400 error](https://platform.claude.com/docs/en/api/errors#forced-tool-use-not-supported) | `auto` with [strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use) to guarantee schema-valid tool inputs, or [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) when you need a response in a fixed JSON shape. Prompting still influences which tool `auto` picks. `none` is also supported |

On models that support it, the highlighted lines are the only difference from a standard tool use request:

<CodeGroup>
  ```bash cURL
  curl -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d @- <<'EOF'
  {
    "model": "claude-opus-5",
    "max_tokens": 1024,
    "tools": [
      {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "tool_choice": {"type": "tool", "name": "get_weather"},
    "messages": [
      {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]
  }
  EOF
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
  tool_choice:
    type: tool
    name: get_weather
  messages:
    - role: user
      content: What's the weather like in San Francisco?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  tools = [
      {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
              "type": "object",
              "properties": {
                  "location": {
                      "type": "string",
                      "description": "The city and state, e.g. San Francisco, CA",
                  }
              },
              "required": ["location"],
          },
      }
  ]

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "tool", "name": "get_weather"},
      messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "tool", name: "get_weather" },
    messages: [{ role: "user", content: "What's the weather like in San Francisco?" }]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Tools = [
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the current weather in a given location",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                  },
                  Required = ["location"],
              },
          }),
      ],
      ToolChoice = new ToolChoiceTool { Name = "get_weather" },
      Messages = [
          new() { Role = Role.User, Content = "What's the weather like in San Francisco?" }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	ToolChoice: anthropic.ToolChoiceUnionParam{OfTool: &anthropic.ToolChoiceToolParam{Name: "get_weather"}},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather like in San Francisco?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolChoice;
  import com.anthropic.models.messages.ToolChoiceTool;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addTool(Tool.builder()
              .name("get_weather")
              .description("Get the current weather in a given location")
              .inputSchema(InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "location", Map.of(
                          "type", "string",
                          "description", "The city and state, e.g. San Francisco, CA"
                      )
                  )))
                  .required(List.of("location"))
                  .build())
              .build())
          .toolChoice(ToolChoice.ofTool(ToolChoiceTool.builder()
              .name("get_weather")
              .build()))
          .addUserMessage("What's the weather like in San Francisco?")
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather like in San Francisco?"]
      ],
      model: 'claude-opus-5',
      toolChoice: ['type' => 'tool', 'name' => 'get_weather'],
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ]
                  ],
                  'required' => ['location']
              ]
          ]
      ],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "tool", name: "get_weather" },
    messages: [
      { role: "user", content: "What's the weather like in San Francisco?" }
    ]
  )
  puts message
  ```
</CodeGroup>

When working with the `tool_choice` parameter, there are four possible options:

* `auto` allows Claude to determine whether to call any provided tools or not. This is the default value when `tools` are provided.
* `any` tells Claude that it must use one of the provided tools, but doesn't force a particular tool.
* `tool` forces Claude to always use a particular tool.
* `none` prevents Claude from using any tools. This is the default value when no `tools` are provided.

<Note>
  When using [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#what-invalidates-the-cache), changes to the `tool_choice` parameter will invalidate cached message blocks. Tool definitions and system prompts remain cached, but message content must be reprocessed.
</Note>

This diagram illustrates how each option works:

<Frame>
  ![Diagram of three tool\_choice options: auto (a tool or a plain response), any (one of the tools), and tool (the named tool)](https://platform.claude.com/docs/images/tool_choice.svg)
</Frame>

Note that when you have `tool_choice` as `any` or `tool`, the API prefills the assistant message to force a tool to be used. This means that the models will not emit a natural language response or explanation before `tool_use` content blocks, even if explicitly asked to do so.

Testing has shown that this should not reduce performance. If you would like the model to provide natural language context or explanations while still requesting that the model use a specific tool, you can use `{"type": "auto"}` for `tool_choice` (the default) and add explicit instructions in a `user` message. For example: `What's the weather like in London? Use the get_weather tool in your response.`

<Tip>
  **Guaranteed tool calls with strict tools**

  On models that support forced tool use, combine `tool_choice: {"type": "any"}` with [strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use) to guarantee both that one of your tools is called and that the tool inputs strictly follow your schema. Set `strict: true` on your tool definitions to enable schema validation.
</Tip>

### Model responses with tools

When using tools, Claude often comments on what it's doing or responds naturally to the user before calling tools.

For example, given the prompt "What's the weather like in San Francisco right now, and what time is it there?", Claude might respond with:

```json JSON
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll help you check the current weather and time in San Francisco."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": { "location": "San Francisco, CA" }
    }
  ]
}
```

This natural response style helps users understand what Claude is doing and creates a more conversational interaction. You can guide the style and content of these responses through your system prompts and by providing `<examples>` in your prompts.

It's important to note that Claude may use various phrasings and approaches when explaining its actions. Your code should treat these responses like any other assistant-generated text, and not rely on specific formatting conventions.

## Next steps

<CardGroup>
  <Card href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls" title="Handle tool calls">
    Parse tool\_use blocks and format tool\_result responses.
  </Card>

  <Card href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner" title="Tool Runner (SDK)">
    Let the SDK handle the agentic loop automatically.
  </Card>

  <Card href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference" title="Tool reference">
    Directory of Anthropic-provided tools and optional properties.
  </Card>
</CardGroup>


---
title: Parallel tool use
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
description: Enable, format, and disable parallel tool calls, with message-history guidance and troubleshooting.
---

By default, Claude may call multiple tools in a single response. This page covers how to run those calls, how to format the message history so parallelism keeps working, and how to disable parallel tool use when you need to. For the single-call flow, see [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

## Execution semantics

When Claude calls tools, the response has a `stop_reason` of `tool_use` and can contain several `tool_use` blocks in a single assistant turn. How you run those calls is your decision. The API doesn't prescribe an execution order: you can run the calls concurrently (`Promise.all`, `asyncio.gather`), sequentially in the order they appear, or in any combination that suits your tools.

Choose the strategy based on what your tools do. Independent, read-only operations are usually safe to run in parallel for lower latency. Tools with side effects, shared state, or ordering requirements might be better run sequentially.

Whichever strategy you use, return one `tool_result` for each `tool_use` block, all together in the next user message. Match each result to its call with `tool_use_id`, and put every `tool_result` block before any text content in that message. See [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) for the full formatting rules. If you choose not to run a particular call (for example, because you ran the batch sequentially and an earlier call failed), still return a `tool_result` for it with `is_error: true` and a brief explanation.

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_02",
  "is_error": true,
  "content": "Not executed: the preceding write_file call failed."
}
```

The [computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#batch-actions) and the [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#batch-actions) are stricter. When Claude returns several of their member tool calls in one turn (a batch action), run them sequentially in the order they appear and stop at the first failure; each tool defines the exact text to return for the calls you skip.

## Test parallel tool calls

<Note>
  **Use the Tool Runner for most applications:** the SDK [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) handles responses with multiple tool calls and formats the results for you, so you don't write this handling yourself. Use the manual pattern on this page when you need direct control over how the calls run, such as custom batching, ordering, or error handling.
</Note>

The following script sends a request that should trigger parallel tool calls, verifies the response contains them, and formats the tool results so parallelism keeps working. Run it with `ANTHROPIC_API_KEY` set in your environment:

<CodeGroup>
  ```bash cURL
  # This end-to-end test flow doesn't translate well to a one-off shell command.
  # See the SDK tabs for the full flow. The underlying HTTP request is a standard
  # tool use request with multiple tools defined.
  ```

  ```bash CLI
  # This end-to-end test flow doesn't translate well to a one-off shell command.
  # See the SDK tabs for the full flow.
  ```

  ```python Python
  client = Anthropic()

  # Define tools
  tools = [
      {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
              "type": "object",
              "properties": {
                  "location": {
                      "type": "string",
                      "description": "The city and state, e.g. San Francisco, CA",
                  }
              },
              "required": ["location"],
          },
      },
      {
          "name": "get_time",
          "description": "Get the current time in a given timezone",
          "input_schema": {
              "type": "object",
              "properties": {
                  "timezone": {
                      "type": "string",
                      "description": "The timezone, e.g. America/New_York",
                  }
              },
              "required": ["timezone"],
          },
      },
  ]

  # Test conversation with parallel tool calls
  messages = [
      {
          "role": "user",
          "content": "What's the weather in SF and NYC, and what time is it there?",
      }
  ]

  # Make initial request
  print("Requesting parallel tool calls...")
  response = client.messages.create(
      model="claude-opus-5-5", max_tokens=1024, messages=messages, tools=tools
  )

  # Check for parallel tool calls
  tool_uses = [block for block in response.content if block.type == "tool_use"]
  print(f"\n✓ Claude made {len(tool_uses)} tool calls")

  if len(tool_uses) > 1:
      print("✓ Parallel tool calls detected!")
      for tool in tool_uses:
          print(f"  - {tool.name}: {tool.input}")
  else:
      print("✗ No parallel tool calls detected")

  # Simulate tool execution and format results correctly
  tool_results = []
  for tool_use in tool_uses:
      if tool_use.name == "get_weather":
          if "San Francisco" in str(tool_use.input):
              result = "San Francisco: 68°F, partly cloudy"
          else:
              result = "New York: 45°F, clear skies"
      else:  # get_time
          if "Los_Angeles" in str(tool_use.input):
              result = "2:30 PM PST"
          else:
              result = "5:30 PM EST"

      tool_results.append(
          {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
      )

  # Continue conversation with tool results
  messages.extend(
      [
          {"role": "assistant", "content": response.content},
          {"role": "user", "content": tool_results},  # All results in one message!
      ]
  )

  # Get final response
  print("\nGetting final response...")
  final_response = client.messages.create(
      model="claude-opus-5-5", max_tokens=1024, messages=messages, tools=tools
  )

  final_text = next(
      block.text for block in final_response.content if block.type == "text"
  )
  print(f"\nClaude's response:\n{final_text}")

  # Verify formatting
  print("\n--- Verification ---")
  print(f"✓ Tool results sent in single user message: {len(tool_results)} results")
  print("✓ No text before tool results in content array")
  print("✓ Conversation formatted correctly for future parallel tool use")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Define tools
  const tools: Anthropic.Tool[] = [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object" as const,
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          }
        },
        required: ["location"]
      }
    },
    {
      name: "get_time",
      description: "Get the current time in a given timezone",
      input_schema: {
        type: "object" as const,
        properties: {
          timezone: {
            type: "string",
            description: "The timezone, e.g. America/New_York"
          }
        },
        required: ["timezone"]
      }
    }
  ];

  // Make initial request
  console.log("Requesting parallel tool calls...");
  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in SF and NYC, and what time is it there?"
      }
    ],
    tools: tools
  });

  // Check for parallel tool calls
  const toolUses = response.content.filter((block) => block.type === "tool_use");
  console.log(`\n✓ Claude made ${toolUses.length} tool calls`);

  if (toolUses.length > 1) {
    console.log("✓ Parallel tool calls detected!");
    for (const tool of toolUses) {
      if (tool.type === "tool_use") {
        console.log(`  - ${tool.name}: ${JSON.stringify(tool.input)}`);
      }
    }
  } else {
    console.log("✗ No parallel tool calls detected");
  }

  // Simulate tool execution and format results correctly
  const toolResults: Anthropic.ToolResultBlockParam[] = toolUses
    .filter((block): block is Anthropic.ToolUseBlock => block.type === "tool_use")
    .map((toolUse) => {
      const input = toolUse.input as Record<string, string>;
      let result: string;
      if (toolUse.name === "get_weather") {
        result = input.location?.includes("San Francisco")
          ? "San Francisco: 68F, partly cloudy"
          : "New York: 45F, clear skies";
      } else {
        result = input.timezone?.includes("Los_Angeles") ? "2:30 PM PST" : "5:30 PM EST";
      }

      return {
        type: "tool_result" as const,
        tool_use_id: toolUse.id,
        content: result
      };
    });

  // Get final response with correct formatting
  console.log("\nGetting final response...");
  const finalResponse = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "What's the weather in SF and NYC, and what time is it there?"
      },
      { role: "assistant", content: response.content },
      { role: "user", content: toolResults }
    ],
    tools: tools
  });

  for (const block of finalResponse.content) {
    if (block.type === "text") {
      console.log(`\nClaude's response:\n${block.text}`);
    }
  }

  // Verify formatting
  console.log("\n--- Verification ---");
  console.log(`✓ Tool results sent in single user message: ${toolResults.length} results`);
  console.log("✓ No text before tool results in content array");
  console.log("✓ Conversation formatted correctly for future parallel tool use");
  ```

  ```csharp C#
  AnthropicClient client = new();

  var tools = new List<ToolUnion>
  {
      new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get the current weather in a given location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
              },
              Required = ["location"],
          },
      }),
      new ToolUnion(new Tool()
      {
          Name = "get_time",
          Description = "Get the current time in a given timezone",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["timezone"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The timezone, e.g. America/New_York" }),
              },
              Required = ["timezone"],
          },
      }),
  };

  Console.WriteLine("Requesting parallel tool calls...");
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "What's the weather in SF and NYC, and what time is it there?" }],
      Tools = tools
  };

  var response = await client.Messages.Create(parameters);

  var toolUses = new List<ToolUseBlock>();
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          toolUses.Add(toolUse);
      }
  }
  Console.WriteLine($"\n✓ Claude made {toolUses.Count} tool calls");

  if (toolUses.Count > 1)
  {
      Console.WriteLine("✓ Parallel tool calls detected!");
      foreach (var tool in toolUses)
      {
          Console.WriteLine($"  - {tool.Name}: {JsonSerializer.Serialize(tool.Input)}");
      }
  }
  else
  {
      Console.WriteLine("✗ No parallel tool calls detected");
  }

  var toolResults = new List<ContentBlockParam>();
  foreach (var toolUse in toolUses)
  {
      string result;
      if (toolUse.Name == "get_weather")
      {
          result = JsonSerializer.Serialize(toolUse.Input).Contains("San Francisco")
              ? "San Francisco: 68°F, partly cloudy"
              : "New York: 45°F, clear skies";
      }
      else
      {
          result = JsonSerializer.Serialize(toolUse.Input).Contains("Los_Angeles")
              ? "2:30 PM PST"
              : "5:30 PM EST";
      }

      toolResults.Add(new ContentBlockParam(new ToolResultBlockParam()
      {
          ToolUseID = toolUse.ID,
          Content = result,
      }));
  }

  Console.WriteLine("\nGetting final response...");
  var finalParameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [
          new() { Role = Role.User, Content = "What's the weather in SF and NYC, and what time is it there?" },
          new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
          new() { Role = Role.User, Content = new MessageParamContent(toolResults) }
      ],
      Tools = tools
  };

  var finalResponse = await client.Messages.Create(finalParameters);
  var text = finalResponse.Content.Select(b => b.Value).OfType<TextBlock>().FirstOrDefault();
  Console.WriteLine($"\nClaude's response:\n{text?.Text}");

  Console.WriteLine("\n--- Verification ---");
  Console.WriteLine($"✓ Tool results sent in single user message: {toolResults.Count} results");
  Console.WriteLine("✓ No text before tool results in content array");
  Console.WriteLine("✓ Conversation formatted correctly for future parallel tool use");
  ```

  ```go Go
  client := anthropic.NewClient()

  tools := []anthropic.ToolUnionParam{
  	{OfTool: &anthropic.ToolParam{
  		Name:        "get_weather",
  		Description: anthropic.String("Get the current weather in a given location"),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"location": map[string]any{
  					"type":        "string",
  					"description": "The city and state, e.g. San Francisco, CA",
  				},
  			},
  			Required: []string{"location"},
  		},
  	}},
  	{OfTool: &anthropic.ToolParam{
  		Name:        "get_time",
  		Description: anthropic.String("Get the current time in a given timezone"),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"timezone": map[string]any{
  					"type":        "string",
  					"description": "The timezone, e.g. America/New_York",
  				},
  			},
  			Required: []string{"timezone"},
  		},
  	}},
  }

  fmt.Println("Requesting parallel tool calls...")
  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in SF and NYC, and what time is it there?")),
  	},
  	Tools: tools,
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Find tool use blocks using type switch
  type toolUseInfo struct {
  	ID    string
  	Name  string
  	Input json.RawMessage
  }
  var toolUses []toolUseInfo
  for _, block := range response.Content {
  	switch variant := block.AsAny().(type) {
  	case anthropic.ToolUseBlock:
  		toolUses = append(toolUses, toolUseInfo{
  			ID:    variant.ID,
  			Name:  variant.Name,
  			Input: variant.Input,
  		})
  	}
  }

  fmt.Printf("\n✓ Claude made %d tool calls\n", len(toolUses))

  if len(toolUses) > 1 {
  	fmt.Println("✓ Parallel tool calls detected!")
  	for _, tool := range toolUses {
  		fmt.Printf("  - %s: %s\n", tool.Name, string(tool.Input))
  	}
  } else {
  	fmt.Println("✗ No parallel tool calls detected")
  }

  // Build tool results
  var toolResults []anthropic.ContentBlockParamUnion
  for _, toolUse := range toolUses {
  	var result string
  	inputStr := string(toolUse.Input)

  	if toolUse.Name == "get_weather" {
  		if strings.Contains(inputStr, "San Francisco") {
  			result = "San Francisco: 68°F, partly cloudy"
  		} else {
  			result = "New York: 45°F, clear skies"
  		}
  	} else {
  		if strings.Contains(inputStr, "Los_Angeles") {
  			result = "2:30 PM PST"
  		} else {
  			result = "5:30 PM EST"
  		}
  	}

  	toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, result, false))
  }

  fmt.Println("\nGetting final response...")
  finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in SF and NYC, and what time is it there?")),
  		response.ToParam(),
  		anthropic.NewUserMessage(toolResults...),
  	},
  	Tools: tools,
  })
  if err != nil {
  	log.Fatal(err)
  }

  var finalText string
  for _, block := range finalResponse.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		finalText = textBlock.Text
  		break
  	}
  }

  fmt.Printf("\nClaude's response:\n%s\n", finalText)

  fmt.Println("\n--- Verification ---")
  fmt.Printf("✓ Tool results sent in single user message: %d results\n", len(toolResults))
  fmt.Println("✓ No text before tool results in content array")
  fmt.Println("✓ Conversation formatted correctly for future parallel tool use")
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Tool weatherTool = Tool.builder()
      .name("get_weather")
      .description("Get the current weather in a given location")
      .inputSchema(InputSchema.builder()
          .properties(JsonValue.from(Map.of(
              "location", Map.of(
                  "type", "string",
                  "description", "The city and state, e.g. San Francisco, CA"
              )
          )))
          .putAdditionalProperty("required", JsonValue.from(List.of("location")))
          .build())
      .build();

  Tool timeTool = Tool.builder()
      .name("get_time")
      .description("Get the current time in a given timezone")
      .inputSchema(InputSchema.builder()
          .properties(JsonValue.from(Map.of(
              "timezone", Map.of(
                  "type", "string",
                  "description", "The timezone, e.g. America/New_York"
              )
          )))
          .putAdditionalProperty("required", JsonValue.from(List.of("timezone")))
          .build())
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .addTool(weatherTool)
      .addTool(timeTool)
      .addUserMessage("What's the weather in SF and NYC, and what time is it there?")
      .build();

  IO.println("Requesting parallel tool calls...");
  Message response = client.messages().create(params);

  List<ToolUseBlock> toolUses = new ArrayList<>();
  for (ContentBlock block : response.content()) {
      if (block.toolUse().isPresent()) {
          toolUses.add(block.toolUse().get());
      }
  }

  IO.println("\n✓ Claude made " + toolUses.size() + " tool calls");

  if (toolUses.size() > 1) {
      IO.println("✓ Parallel tool calls detected!");
      for (ToolUseBlock tool : toolUses) {
          IO.println("  - " + tool.name() + ": " + tool._input());
      }
  } else {
      IO.println("✗ No parallel tool calls detected");
  }

  List<ContentBlockParam> toolResults = new ArrayList<>();
  for (ToolUseBlock toolUse : toolUses) {
      String result;
      if (toolUse.name().equals("get_weather")) {
          String location = toolUse._input().toString();
          result = location.contains("San Francisco")
              ? "San Francisco: 68°F, partly cloudy"
              : "New York: 45°F, clear skies";
      } else {
          String timezone = toolUse._input().toString();
          result = timezone.contains("Los_Angeles")
              ? "2:30 PM PST"
              : "5:30 PM EST";
      }
      toolResults.add(ContentBlockParam.ofToolResult(
          ToolResultBlockParam.builder()
              .toolUseId(toolUse.id())
              .content(result)
              .build()
      ));
  }

  IO.println("\nGetting final response...");
  MessageCreateParams finalParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .addTool(weatherTool)
      .addTool(timeTool)
      .addUserMessage("What's the weather in SF and NYC, and what time is it there?")
      .addMessage(response)
      .addUserMessageOfBlockParams(toolResults)
      .build();

  Message finalResponse = client.messages().create(finalParams);
  finalResponse.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> IO.println("\nClaude's response:\n" + textBlock.text()));

  IO.println("\n--- Verification ---");
  IO.println("✓ Tool results sent in single user message: " + toolResults.size() + " results");
  IO.println("✓ No text before tool results in content array");
  IO.println("✓ Conversation formatted correctly for future parallel tool use");
  ```

  ```php PHP
  $client = new Client();

  $tools = [
      [
          'name' => 'get_weather',
          'description' => 'Get the current weather in a given location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => [
                      'type' => 'string',
                      'description' => 'The city and state, e.g. San Francisco, CA'
                  ]
              ],
              'required' => ['location']
          ]
      ],
      [
          'name' => 'get_time',
          'description' => 'Get the current time in a given timezone',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'timezone' => [
                      'type' => 'string',
                      'description' => 'The timezone, e.g. America/New_York'
                  ]
              ],
              'required' => ['timezone']
          ]
      ]
  ];

  echo "Requesting parallel tool calls...\n";
  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather in SF and NYC, and what time is it there?"]
      ],
      model: 'claude-opus-5-5',
      tools: $tools,
  );

  $toolUses = array_filter($response->content, fn($block) => $block->type === 'tool_use');
  echo "\n✓ Claude made " . count($toolUses) . " tool calls\n";

  if (count($toolUses) > 1) {
      echo "✓ Parallel tool calls detected!\n";
      foreach ($toolUses as $tool) {
          echo "  - {$tool->name}: " . json_encode($tool->input) . "\n";
      }
  } else {
      echo "✗ No parallel tool calls detected\n";
  }

  $toolResults = [];
  foreach ($toolUses as $toolUse) {
      if ($toolUse->name === 'get_weather') {
          $result = str_contains(json_encode($toolUse->input), 'San Francisco')
              ? 'San Francisco: 68°F, partly cloudy'
              : 'New York: 45°F, clear skies';
      } else {
          $result = str_contains(json_encode($toolUse->input), 'Los_Angeles')
              ? '2:30 PM PST'
              : '5:30 PM EST';
      }

      $toolResults[] = [
          'type' => 'tool_result',
          'tool_use_id' => $toolUse->id,
          'content' => $result
      ];
  }

  echo "\nGetting final response...\n";
  $finalResponse = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => "What's the weather in SF and NYC, and what time is it there?"],
          ['role' => 'assistant', 'content' => $response->content],
          ['role' => 'user', 'content' => $toolResults]
      ],
      model: 'claude-opus-5-5',
      tools: $tools,
  );

  $textBlock = array_find($finalResponse->content, static fn ($block): bool => $block->type === 'text');
  echo "\nClaude's response:\n{$textBlock->text}\n";

  echo "\n--- Verification ---\n";
  echo "✓ Tool results sent in single user message: " . count($toolResults) . " results\n";
  echo "✓ No text before tool results in content array\n";
  echo "✓ Conversation formatted correctly for future parallel tool use\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  tools = [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          }
        },
        required: ["location"]
      }
    },
    {
      name: "get_time",
      description: "Get the current time in a given timezone",
      input_schema: {
        type: "object",
        properties: {
          timezone: {
            type: "string",
            description: "The timezone, e.g. America/New_York"
          }
        },
        required: ["timezone"]
      }
    }
  ]

  puts "Requesting parallel tool calls..."
  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" }
    ],
    tools: tools
  )

  tool_uses = response.content.select { |block| block.type == :tool_use }
  puts "\n✓ Claude made #{tool_uses.length} tool calls"

  if tool_uses.length > 1
    puts "✓ Parallel tool calls detected!"
    tool_uses.each do |tool|
      puts "  - #{tool.name}: #{tool.input}"
    end
  else
    puts "✗ No parallel tool calls detected"
  end

  tool_results = tool_uses.map do |tool_use|
    result = if tool_use.name == "get_weather"
      location = tool_use.input[:location].to_s
      location.include?("San Francisco") ? "San Francisco: 68°F, partly cloudy" : "New York: 45°F, clear skies"
    else
      timezone = tool_use.input[:timezone].to_s
      timezone.include?("Los_Angeles") ? "2:30 PM PST" : "5:30 PM EST"
    end

    {
      type: "tool_result",
      tool_use_id: tool_use.id,
      content: result
    }
  end

  puts "\nGetting final response..."
  final_response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" },
      { role: "assistant", content: response.content },
      { role: "user", content: tool_results }
    ],
    tools: tools
  )

  final_text = final_response.content.find { |block| block.type == :text }
  puts "\nClaude's response:\n#{final_text.text}"

  puts "\n--- Verification ---"
  puts "✓ Tool results sent in single user message: #{tool_results.length} results"
  puts "✓ No text before tool results in content array"
  puts "✓ Conversation formatted correctly for future parallel tool use"
  ```
</CodeGroup>

The summary lines at the end restate the two formatting rules that keep parallelism working: every tool result returns in a single user message, and no text content appears before the tool results in that message.

## Maximizing parallel tool use

Claude 4 and later models make parallel tool calls by default when a request benefits from multiple tools. For all models, you can increase the likelihood of parallel tool calls with targeted prompting:

<AccordionGroup>
  <Accordion title="System prompts for parallel tool use">
    For Claude 4 and later models, add this to your system prompt:

    ```text wrap
    For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
    ```

    For even stronger parallel tool use (recommended if the default isn't sufficient), use:

    ```text wrap
    <use_parallel_tool_calls>
    For maximum efficiency, whenever you perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially. Prioritize calling tools in parallel whenever possible. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. When running multiple read-only commands like `ls` or `list_dir`, always run all of the commands in parallel. Err on the side of maximizing parallel tool calls rather than running too many tools sequentially.
    </use_parallel_tool_calls>
    ```
  </Accordion>

  <Accordion title="User message prompting">
    You can also encourage parallel tool use within specific user messages:

    ```text wrap
    Instead of:
    "What's the weather in Paris? Also check London."

    Use:
    "Check the weather in Paris and London simultaneously."

    Or be explicit:
    "Please use parallel tool calls to get the weather for Paris, London, and Tokyo at the same time."
    ```
  </Accordion>
</AccordionGroup>

<Note>
  **Claude Fable 5.1 in long agent loops**

  Claude Fable 5.1 may issue fewer parallel tool calls than earlier models, most noticeably in long agent loops where the next reads are only implied (custom coding agents, bash and text editor harnesses, computer use). Standard function calling is unaffected. For the batching instruction to add and where to put it, see [Batch independent tool calls in agent loops](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#batch-independent-tool-calls-in-agent-loops).
</Note>

## Disable parallel tool use

Parallel tool use is on by default. To turn it off, set `disable_parallel_tool_use: true` inside the [`tool_choice`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use) object. It is not a top-level request parameter. The effect depends on the `tool_choice` type.

### At most one tool call

When `tool_choice` type is `auto` (the default), setting `disable_parallel_tool_use: true` means Claude calls at most one tool per response. Claude can still answer in plain text without calling any tool. The highlighted lines are the only change from a standard tool use request:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }],
      "tool_choice": {"type": "auto", "disable_parallel_tool_use": true},
      "messages": [
        {"role": "user", "content": "What is the weather in San Francisco and New York?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
  tool_choice:
    type: auto
    disable_parallel_tool_use: true
  messages:
    - role: user
      content: What is the weather in San Francisco and New York?
  YAML
  ```

  ```python Python
  client = Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA",
                      }
                  },
                  "required": ["location"],
              },
          }
      ],
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=[
          {
              "role": "user",
              "content": "What is the weather in San Francisco and New York?",
          }
      ],
  )
  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages: [{ role: "user", content: "What is the weather in San Francisco and New York?" }]
  });
  console.log(response.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Tools = [
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the current weather in a given location",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                  },
                  Required = ["location"],
              },
          }),
      ],
      ToolChoice = new ToolChoiceAuto { DisableParallelToolUse = true },
      Messages = [new() { Role = Role.User, Content = "What is the weather in San Francisco and New York?" }]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	ToolChoice: anthropic.ToolChoiceUnionParam{
  		OfAuto: &anthropic.ToolChoiceAutoParam{
  			DisableParallelToolUse: anthropic.Bool(true),
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco and New York?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  InputSchema schema = InputSchema.builder()
      .properties(
          JsonValue.from(
              Map.of(
                  "location", Map.of(
                      "type", "string",
                      "description", "The city and state, e.g. San Francisco, CA"
                  )
              )
          )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .addTool(
          Tool.builder()
              .name("get_weather")
              .description("Get the current weather in a given location")
              .inputSchema(schema)
              .build()
      )
      .toolChoice(ToolChoiceAuto.builder().disableParallelToolUse(true).build())
      .addUserMessage("What is the weather in San Francisco and New York?")
      .build();

  Message response = client.messages().create(params);
  IO.println(response.content());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'What is the weather in San Francisco and New York?']
      ],
      model: 'claude-opus-5-5',
      toolChoice: ['type' => 'auto', 'disableParallelToolUse' => true],
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ]
                  ],
                  'required' => ['location']
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages: [
      { role: "user", content: "What is the weather in San Francisco and New York?" }
    ]
  )
  puts response.content
  ```
</CodeGroup>

### Exactly one tool call

When `tool_choice` type is `any` or `tool`, setting `disable_parallel_tool_use: true` means Claude calls exactly one tool. Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 don't support these `tool_choice` types (see [Forcing tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use)). The following example uses `any`. The same field works with `tool`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }],
      "tool_choice": {"type": "any", "disable_parallel_tool_use": true},
      "messages": [
        {"role": "user", "content": "What is the weather in San Francisco and New York?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
  tool_choice:
    type: any
    disable_parallel_tool_use: true
  messages:
    - role: user
      content: What is the weather in San Francisco and New York?
  YAML
  ```

  ```python Python
  client = Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA",
                      }
                  },
                  "required": ["location"],
              },
          }
      ],
      tool_choice={"type": "any", "disable_parallel_tool_use": True},
      messages=[
          {
              "role": "user",
              "content": "What is the weather in San Francisco and New York?",
          }
      ],
  )
  print(response.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "any", disable_parallel_tool_use: true },
    messages: [{ role: "user", content: "What is the weather in San Francisco and New York?" }]
  });
  console.log(response.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Tools = [
          new ToolUnion(new Tool()
          {
              Name = "get_weather",
              Description = "Get the current weather in a given location",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                  },
                  Required = ["location"],
              },
          }),
      ],
      ToolChoice = new ToolChoiceAny { DisableParallelToolUse = true },
      Messages = [new() { Role = Role.User, Content = "What is the weather in San Francisco and New York?" }]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	ToolChoice: anthropic.ToolChoiceUnionParam{
  		OfAny: &anthropic.ToolChoiceAnyParam{
  			DisableParallelToolUse: anthropic.Bool(true),
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco and New York?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  InputSchema schema = InputSchema.builder()
      .properties(
          JsonValue.from(
              Map.of(
                  "location", Map.of(
                      "type", "string",
                      "description", "The city and state, e.g. San Francisco, CA"
                  )
              )
          )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024L)
      .addTool(
          Tool.builder()
              .name("get_weather")
              .description("Get the current weather in a given location")
              .inputSchema(schema)
              .build()
      )
      .toolChoice(ToolChoiceAny.builder().disableParallelToolUse(true).build())
      .addUserMessage("What is the weather in San Francisco and New York?")
      .build();

  Message response = client.messages().create(params);
  IO.println(response.content());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'What is the weather in San Francisco and New York?']
      ],
      model: 'claude-opus-5',
      toolChoice: ['type' => 'any', 'disableParallelToolUse' => true],
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ]
                  ],
                  'required' => ['location']
              ]
          ]
      ],
  );

  echo $response;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    tool_choice: { type: "any", disable_parallel_tool_use: true },
    messages: [
      { role: "user", content: "What is the weather in San Francisco and New York?" }
    ]
  )
  puts response.content
  ```
</CodeGroup>

## Troubleshooting

If Claude isn't making parallel tool calls when expected, check these common issues:

**1. Incorrect tool result formatting**

The most common issue is formatting tool results incorrectly in the conversation history. This "teaches" Claude to avoid parallel calls.

Specifically for parallel tool use:

* **Wrong:** a separate user message for each tool result
* **Correct:** all tool results together in a single user message

```json
// Wrong: separate user messages reduce parallel tool use
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1]},
  {"role": "user", "content": [tool_result_2]}  // Separate message
]

// Correct: one user message with all results maintains parallel tool use
[
  {"role": "assistant", "content": [tool_use_1, tool_use_2]},
  {"role": "user", "content": [tool_result_1, tool_result_2]}  // Single message
]
```

See [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) for other formatting rules.

**2. Weak prompting**

Default prompting might not be sufficient. Use the stronger system prompt from [Maximizing parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use#maximizing-parallel-tool-use).

**3. Measuring parallel tool usage**

To verify parallel tool calls are working:

<CodeGroup>
  ```bash cURL
  # Measuring parallel tool use is client-side analysis of responses you've already
  # collected, so it doesn't translate to a one-off shell command. See the SDK tabs.
  ```

  ```bash CLI
  # Measuring parallel tool use is client-side analysis of responses you've already
  # collected, so it doesn't translate to a one-off shell command. See the SDK tabs.
  ```

  ```python Python
  messages = []  # Message objects returned by client.messages.create across your run

  tool_call_messages = [
      msg for msg in messages if any(block.type == "tool_use" for block in msg.content)
  ]
  total_tool_calls = sum(
      len([block for block in msg.content if block.type == "tool_use"])
      for msg in tool_call_messages
  )
  avg_tools_per_message = (
      total_tool_calls / len(tool_call_messages) if tool_call_messages else 0.0
  )
  print(f"Average tools per message: {avg_tools_per_message}")
  # Should be > 1.0 if parallel calls are working
  ```

  ```typescript TypeScript
  const messages: Anthropic.Message[] = []; // Message objects returned by client.messages.create across your run

  const toolCallMessages = messages.filter((message) =>
    message.content.some((block) => block.type === "tool_use")
  );
  const totalToolCalls = toolCallMessages.reduce(
    (sum, message) => sum + message.content.filter((block) => block.type === "tool_use").length,
    0
  );
  const avgToolsPerMessage =
    toolCallMessages.length > 0 ? totalToolCalls / toolCallMessages.length : 0;
  console.log(`Average tools per message: ${avgToolsPerMessage}`);
  // Should be > 1.0 if parallel calls are working
  ```

  ```csharp C#
  List<Message> messages = []; // Message objects returned by client.Messages.Create across your run

  var toolCallMessages = messages
      .Where(message => message.Content.Any(block => block.TryPickToolUse(out _)))
      .ToList();
  var totalToolCalls = toolCallMessages
      .Sum(message => message.Content.Count(block => block.TryPickToolUse(out _)));
  var avgToolsPerMessage = toolCallMessages.Count > 0 ? (double)totalToolCalls / toolCallMessages.Count : 0.0;
  Console.WriteLine($"Average tools per message: {avgToolsPerMessage}");
  // Should be > 1.0 if parallel calls are working
  ```

  ```go Go
  var messages []anthropic.Message // Message values returned by client.Messages.New across your run

  toolCallMessageCount := 0
  totalToolCalls := 0
  for _, message := range messages {
  	callsInMessage := 0
  	for _, block := range message.Content {
  		if block.Type == "tool_use" {
  			callsInMessage++
  		}
  	}
  	if callsInMessage > 0 {
  		toolCallMessageCount++
  		totalToolCalls += callsInMessage
  	}
  }

  avgToolsPerMessage := 0.0
  if toolCallMessageCount > 0 {
  	avgToolsPerMessage = float64(totalToolCalls) / float64(toolCallMessageCount)
  }
  fmt.Println("Average tools per message:", avgToolsPerMessage)
  // Should be > 1.0 if parallel calls are working
  ```

  ```java Java
  List<Message> messages = List.of(); // Message objects returned by client.messages().create() across your run

  List<Message> toolCallMessages = messages.stream()
      .filter(message -> message.content().stream().anyMatch(ContentBlock::isToolUse))
      .toList();
  long totalToolCalls = toolCallMessages.stream()
      .mapToLong(message -> message.content().stream().filter(ContentBlock::isToolUse).count())
      .sum();
  double avgToolsPerMessage = toolCallMessages.isEmpty() ? 0.0 : (double) totalToolCalls / toolCallMessages.size();
  IO.println("Average tools per message: " + avgToolsPerMessage);
  // Should be > 1.0 if parallel calls are working
  ```

  ```php PHP
  // $messages: Message objects returned by $client->messages->create() across your run
  $messages = [];

  $toolCallMessages = array_values(array_filter(
      $messages,
      fn ($message) => count(array_filter($message->content, fn ($block) => $block->type === 'tool_use')) > 0
  ));
  $totalToolCalls = array_sum(array_map(
      fn ($message) => count(array_filter($message->content, fn ($block) => $block->type === 'tool_use')),
      $toolCallMessages
  ));
  $avgToolsPerMessage = count($toolCallMessages) > 0 ? $totalToolCalls / count($toolCallMessages) : 0.0;
  echo "Average tools per message: {$avgToolsPerMessage}\n";
  // Should be > 1.0 if parallel calls are working
  ```

  ```ruby Ruby
  messages = [] # Message objects returned by client.messages.create across your run

  tool_call_messages = messages.select { |message| message.content.any? { |block| block.type == :tool_use } }
  total_tool_calls = tool_call_messages.sum { |message| message.content.count { |block| block.type == :tool_use } }
  avg_tools_per_message = tool_call_messages.empty? ? 0.0 : total_tool_calls.to_f / tool_call_messages.size
  puts "Average tools per message: #{avg_tools_per_message}"
  # Should be > 1.0 if parallel calls are working
  ```
</CodeGroup>

**4. Calls in a batch appear to depend on each other**

Execution order is your choice. If your tools have ordering dependencies, running the batch sequentially and stopping on the first failure is a valid strategy (and the required one for the [computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#batch-actions) and [browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#batch-actions) tools): return `is_error: true` for any call you didn't run. If you run in parallel and a call fails because its prerequisite hadn't completed, return `is_error: true` with the natural error message. Claude will reissue the call on the next turn. To reduce dependent calls appearing together, add this to your system prompt: "Only batch tool calls that are independent of each other."

## Next steps

<CardGroup cols={3}>
  <Card title="Tool Runner (SDK)" icon="wrench" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner">
    Use the SDK's Tool Runner abstraction to handle the agentic loop, error wrapping, and type safety automatically.
  </Card>

  <Card title="Handle tool calls" icon="arrows-left-right" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls">
    Parse tool\_use blocks, format tool\_result responses, and handle errors with is\_error.
  </Card>

  <Card title="Define tools" icon="hammer" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools">
    Specify tool schemas, write effective descriptions, and control when Claude calls your tools.
  </Card>
</CardGroup>

Export all of my stored memories and any context you've learned about me from past conversations. Preserve my words verbatim where possible, especially for instructions and preferences.

## Categories (output in this order):

1. **Instructions**: Rules I've explicitly asked you to follow going forward — tone, format, style, "always do X", "never do Y", and corrections to your behavior. Only include rules from stored memories, not from conversations.

2. **Identity**: Name, age, location, education, family, relationships, languages, and personal interests.

3. **Career**: Current and past roles, companies, and general skill areas.

4. **Projects**: Projects I meaningfully built or committed to. Ideally ONE entry per project. Include what it does, current status, and any key decisions. Use the project name or a short descriptor as the first words of the entry.

5. **Preferences**: Opinions, tastes, and working-style preferences that apply broadly.

## Format:

Use section headers for each category. Within each category, list one entry per line, sorted by oldest date first. Format each line as:

[YYYY-MM-DD] - Entry content here.

If no date is known, use [unknown] instead.

## Output:
- Wrap the entire export in a single code block for easy copying.
- After the code block, state whether this is the complete set or if more remain.

---
title: Memory tool
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
description: Let Claude store and retrieve information across conversations by implementing the memory tool's file operations in your application.
---

The memory tool lets Claude store and retrieve information across conversations in a directory of memory files. Claude can create, read, update, and delete files that persist between sessions, building up knowledge over time without keeping everything in the context window.

Memory supports just-in-time context retrieval. Rather than loading all relevant information up front, an agent records what it learns in memory files and reads them back on demand. This keeps the active context focused on the current task, which matters for long-running sessions that would otherwise overwhelm the context window. See [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) for the broader pattern.

The memory tool operates client-side: Claude requests file operations, and your application executes them. You control where and how the data is stored through your own infrastructure.

<Note>
  Reach out through the [feedback form](https://forms.gle/YXC2EKGMhjN1c4L88) to share your feedback on this feature.
</Note>

<Note>
  To learn how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

## Use cases

* Maintain project context across multiple agent sessions
* Apply lessons from past interactions, decisions, and feedback to new tasks
* Build up a knowledge base over time

## How it works

When the memory tool is enabled, Claude automatically checks its memory directory before starting a task. As it works, Claude stores what it learns in files under `/memories` and reads them back in later conversations to continue earlier work.

Because the memory tool is client-side, Claude only requests memory operations. Your application executes each request against storage you control and returns the result in a `tool_result` block (see [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)). The `/memories` path is a prefix that your handler maps onto real storage, such as a per-user directory or keys in a database. Memory lives entirely in your application. A later conversation continues from the same memory when it sends the same `tools` entry and your handler serves the same store. For security, restrict all memory operations to the `/memories` directory (see [Path traversal protection](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#path-traversal-protection)).

### Example: How memory tool calls work

A typical interaction looks like this:

**1. User request:**

```text wrap
"Help me respond to this customer service ticket."
```

**2. Claude checks the memory directory:**

```text wrap
"I'll help you respond to the customer service ticket. Let me check my memory for any previous context."
```

Claude calls the memory tool:

```json
{
  "type": "tool_use",
  "id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "name": "memory",
  "input": {
    "command": "view",
    "path": "/memories"
  }
}
```

**3. Your application returns the directory contents:**

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "content": "Here're the files and directories up to 2 levels deep in /memories, excluding hidden items and node_modules:\n4.0K\t/memories\n1.5K\t/memories/customer_service_guidelines.xml\n2.0K\t/memories/refund_policies.xml"
}
```

**4. Claude reads relevant files:**

```json
{
  "type": "tool_use",
  "id": "toolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "name": "memory",
  "input": {
    "command": "view",
    "path": "/memories/customer_service_guidelines.xml"
  }
}
```

**5. Your application returns the file contents:**

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "content": "Here's the content of /memories/customer_service_guidelines.xml with line numbers:\n     1\t<guidelines>\n     2\t<addressing_customers>\n     3\t- Always address customers by their first name\n     4\t- Use empathetic language\n..."
}
```

**6. Claude uses the memory to help:**

```text wrap
"Based on your customer service guidelines, I can help you craft a response. Please share the ticket details..."
```

The memory tool is available on all Claude 4 and later models. For the full list of Anthropic-provided tools, see the [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference).

## Getting started

Using the memory tool takes two steps:

1. Add the memory tool to your request. The `tools` entry `{"type": "memory_20250818", "name": "memory"}` is the entire configuration: the `name` must be `memory`, and you don't define an input schema for an Anthropic-provided tool.
2. Implement a client-side handler for each memory command. Your handler must reject paths outside `/memories`, so read [Path traversal protection](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#path-traversal-protection) before you write it.

## Basic usage

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 2048,
      "messages": [
        {
          "role": "user",
          "content": "Help me respond to this customer service ticket."
        }
      ],
      "tools": [{
        "type": "memory_20250818",
        "name": "memory"
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 2048
  tools:
    - type: memory_20250818
      name: memory
  messages:
    - role: user
      content: Help me respond to this customer service ticket.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=2048,
      messages=[
          {
              "role": "user",
              "content": "Help me respond to this customer service ticket.",
          }
      ],
      tools=[{"type": "memory_20250818", "name": "memory"}],
  )

  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const message = await anthropic.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "Help me respond to this customer service ticket."
      }
    ],
    tools: [{ type: "memory_20250818", name: "memory" }]
  });

  console.log(message);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var message = await client.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 2048,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Help me respond to this customer service ticket.",
              },
          ],
          Tools = [new MemoryTool20250818()],
      }
  );

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 2048,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Help me respond to this customer service ticket.")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfMemoryTool20250818: &anthropic.MemoryTool20250818Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.models.messages.MemoryTool20250818;
  // ...
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(2048L)
      .addTool(MemoryTool20250818.builder().build())
      .addUserMessage("Help me respond to this customer service ticket.")
      .build();

    Message message = client.messages().create(params);
    IO.println(message);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 2048,
      messages: [
          [
              'role' => 'user',
              'content' => 'Help me respond to this customer service ticket.',
          ],
      ],
      tools: [new MemoryTool20250818],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "Help me respond to this customer service ticket."
      }
    ],
    tools: [
      {
        type: "memory_20250818",
        name: "memory"
      }
    ]
  )
  puts message
  ```
</CodeGroup>

## Implement the memory handler

Claude's reply to a request like the previous one ends with a `tool_use` block that requests a memory operation, such as `view /memories`. Your application executes the operation and returns the result in a `tool_result` block, then sends the conversation back so Claude can continue: the standard [tool-use loop](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

Four SDKs provide memory tool helpers that handle the tool interface and the loop. Subclass `BetaAbstractMemoryTool` (Python and C#), use `betaMemoryTool` (TypeScript), or implement `BetaMemoryToolHandler` (Java) to back memory with your own storage, such as files on disk, a database, cloud storage, or encrypted files. Python and TypeScript also ship a ready-made local-filesystem implementation, `BetaLocalFilesystemMemoryTool`. The helper and tool-runner surfaces live in your SDK's beta namespace even though the memory tool itself doesn't require a beta header. The Go and Ruby SDKs have no memory helper, so those examples run the tool-use loop themselves, and PHP wraps your handler closure in its generic `BetaRunnableTool`. All three use an in-memory store that you replace with your own storage.

<CodeGroup exclude="shell">
  ```python Python
  import anthropic
  from anthropic.tools import BetaLocalFilesystemMemoryTool

  client = anthropic.Anthropic()
  memory = BetaLocalFilesystemMemoryTool(base_path="./memory")

  runner = client.beta.messages.tool_runner(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Remember that customer Acme Corp prefers email follow-ups.",
          }
      ],
      tools=[memory],
  )

  final_message = runner.until_done()
  print(final_message.content)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { betaMemoryTool } from "@anthropic-ai/sdk/helpers/beta/memory";
  import { BetaLocalFilesystemMemoryTool } from "@anthropic-ai/sdk/tools/memory/node";

  const client = new Anthropic();

  const backend = await BetaLocalFilesystemMemoryTool.init("./memory");
  const memory = betaMemoryTool(backend); // or pass your own handlers object

  const runner = client.beta.messages.toolRunner({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Remember that customer Acme Corp prefers email follow-ups."
      }
    ],
    tools: [memory],
    max_iterations: 10
  });

  const finalMessage = await runner;
  console.log(finalMessage.content);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Helpers.Beta;
  using Anthropic.Models.Beta.Messages;

  var client = new AnthropicClient();

  // Your subclass of BetaAbstractMemoryTool
  var memory = new FilesystemMemoryTool("./memories");

  var runner = client.Beta.Messages.ToolRunner(
      new MessageCreateParams
      {
          Model = Anthropic.Models.Messages.Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Remember that customer Acme Corp prefers email follow-ups.",
              },
          ],
      },
      [memory],
      maxIterations: 10
  );

  var finalMessage = await runner.RunUntilDoneAsync();
  Console.WriteLine(finalMessage);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"
  	"slices"
  	"sort"
  	"strings"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  // An in-memory store that maps memory file paths to their contents.
  // Use your own storage in production.
  var store = map[string]string{}

  type memoryCommand struct {
  	Command    string `json:"command"`
  	Path       string `json:"path"`
  	FileText   string `json:"file_text"`
  	OldStr     string `json:"old_str"`
  	NewStr     string `json:"new_str"`
  	InsertLine int    `json:"insert_line"`
  	InsertText string `json:"insert_text"`
  	OldPath    string `json:"old_path"`
  	NewPath    string `json:"new_path"`
  }

  func executeMemory(raw json.RawMessage) string {
  	var cmd memoryCommand
  	if err := json.Unmarshal(raw, &cmd); err != nil {
  		return "Error: invalid memory command"
  	}
  	switch cmd.Command {
  	case "view":
  		if content, ok := store[cmd.Path]; ok {
  			lines := strings.Split(strings.TrimSuffix(content, "\n"), "\n")
  			for i, line := range lines {
  				lines[i] = fmt.Sprintf("%6d\t%s", i+1, line)
  			}
  			return fmt.Sprintf("Here's the content of %s with line numbers:\n%s", cmd.Path, strings.Join(lines, "\n"))
  		}
  		if cmd.Path == "/memories" {
  			listing := []string{"1.0K\t/memories"}
  			for path := range store {
  				listing = append(listing, "1.0K\t"+path)
  			}
  			sort.Strings(listing[1:])
  			return fmt.Sprintf("Here're the files and directories up to 2 levels deep in %s, excluding hidden items and node_modules:\n%s", cmd.Path, strings.Join(listing, "\n"))
  		}
  		return fmt.Sprintf("The path %s does not exist. Please provide a valid path.", cmd.Path)
  	case "create":
  		store[cmd.Path] = cmd.FileText
  		return "File created successfully at: " + cmd.Path
  	case "str_replace":
  		content, ok := store[cmd.Path]
  		if !ok || !strings.Contains(content, cmd.OldStr) {
  			return fmt.Sprintf("No replacement was performed, old_str `%s` did not appear verbatim in %s.", cmd.OldStr, cmd.Path)
  		}
  		store[cmd.Path] = strings.Replace(content, cmd.OldStr, cmd.NewStr, 1)
  		return "The memory file has been edited."
  	case "insert":
  		content, ok := store[cmd.Path]
  		if !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.Path)
  		}
  		lines := strings.Split(content, "\n")
  		if cmd.InsertLine < 0 || cmd.InsertLine > len(lines) {
  			return fmt.Sprintf("Error: Invalid `insert_line` parameter: %d. It should be within the range of lines of the file: [0, %d]", cmd.InsertLine, len(lines))
  		}
  		lines = slices.Insert(lines, cmd.InsertLine, strings.TrimSuffix(cmd.InsertText, "\n"))
  		store[cmd.Path] = strings.Join(lines, "\n")
  		return fmt.Sprintf("The file %s has been edited.", cmd.Path)
  	case "delete":
  		if _, ok := store[cmd.Path]; !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.Path)
  		}
  		delete(store, cmd.Path)
  		return "Successfully deleted " + cmd.Path
  	case "rename":
  		if _, ok := store[cmd.OldPath]; !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.OldPath)
  		}
  		if _, ok := store[cmd.NewPath]; ok {
  			return fmt.Sprintf("Error: The destination %s already exists", cmd.NewPath)
  		}
  		store[cmd.NewPath] = store[cmd.OldPath]
  		delete(store, cmd.OldPath)
  		return fmt.Sprintf("Successfully renamed %s to %s", cmd.OldPath, cmd.NewPath)
  	default:
  		return "Error: unknown command " + cmd.Command
  	}
  }

  func main() {
  	client := anthropic.NewClient()
  	tools := []anthropic.ToolUnionParam{{OfMemoryTool20250818: &anthropic.MemoryTool20250818Param{}}}
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Remember that customer Acme Corp prefers email follow-ups.")),
  	}

  	for {
  		message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5_5,
  			MaxTokens: 1024,
  			Messages:  messages,
  			Tools:     tools,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		if message.StopReason != anthropic.StopReasonToolUse {
  			for _, block := range message.Content {
  				if block.Type == "text" {
  					fmt.Println(block.Text)
  				}
  			}
  			break
  		}
  		results := []anthropic.ContentBlockParamUnion{}
  		for _, block := range message.Content {
  			if block.Type == "tool_use" {
  				results = append(results, anthropic.NewToolResultBlock(block.ID, executeMemory(block.Input), false))
  			}
  		}
  		messages = append(messages, message.ToParam(), anthropic.NewUserMessage(results...))
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.helpers.BetaMemoryToolHandler;
  import com.anthropic.helpers.BetaToolRunner;
  import com.anthropic.models.beta.messages.BetaMemoryTool20250818;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.MessageCreateParams; // beta package, not models.messages
  import com.anthropic.models.beta.messages.ToolRunnerCreateParams;
  import com.anthropic.models.messages.Model;
  import java.nio.file.Path;

  void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Your BetaMemoryToolHandler implementation of the six memory commands
    BetaMemoryToolHandler handler = new FileSystemMemoryToolHandler(Path.of("memories"));

    MessageCreateParams createParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .addTool(BetaMemoryTool20250818.builder().build())
      .addUserMessage("Remember that customer Acme Corp prefers email follow-ups.")
      .build();

    ToolRunnerCreateParams runnerParams = ToolRunnerCreateParams.builder()
      .betaMemoryToolHandler(handler)
      .initialMessageParams(createParams)
      .maxIterations(10)
      .build();

    BetaToolRunner runner = client.beta().messages().toolRunner(runnerParams);
    for (BetaMessage message : runner) {
      IO.println(message);
    }
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Beta\Messages\BetaMemoryTool20250818;
  use Anthropic\Client;
  use Anthropic\Lib\Tools\BetaRunnableTool;
  use Anthropic\Messages\Model;

  $client = new Client();

  // An in-memory store that maps memory file paths to their contents.
  // Use your own storage in production.
  $store = [];

  $memory = new BetaRunnableTool(
      definition: new BetaMemoryTool20250818,
      run: function (array $input) use (&$store): string {
          $path = $input['path'] ?? '';
          switch ($input['command']) {
              case 'view':
                  if (isset($store[$path])) {
                      $numbered = [];
                      foreach (explode("\n", preg_replace('/\n\z/', '', $store[$path])) as $i => $line) {
                          $numbered[] = sprintf("%6d\t%s", $i + 1, $line);
                      }
                      return "Here's the content of {$path} with line numbers:\n" . implode("\n", $numbered);
                  }
                  if ($path === '/memories') {
                      $listing = ["1.0K\t/memories"];
                      foreach (array_keys($store) as $stored) {
                          $listing[] = "1.0K\t{$stored}";
                      }
                      return "Here're the files and directories up to 2 levels deep in {$path}, excluding hidden items and node_modules:\n" . implode("\n", $listing);
                  }
                  return "The path {$path} does not exist. Please provide a valid path.";
              case 'create':
                  $store[$path] = $input['file_text'];
                  return "File created successfully at: {$path}";
              case 'str_replace':
                  $position = strpos($store[$path] ?? '', $input['old_str']);
                  if ($position === false) {
                      return "No replacement was performed, old_str `{$input['old_str']}` did not appear verbatim in {$path}.";
                  }
                  $store[$path] = substr_replace($store[$path], $input['new_str'] ?? '', $position, strlen($input['old_str']));
                  return 'The memory file has been edited.';
              case 'insert':
                  if (!isset($store[$path])) {
                      return "Error: The path {$path} does not exist";
                  }
                  $lines = explode("\n", $store[$path]);
                  if ($input['insert_line'] < 0 || $input['insert_line'] > count($lines)) {
                      return "Error: Invalid `insert_line` parameter: {$input['insert_line']}. It should be within the range of lines of the file: [0, " . count($lines) . "]";
                  }
                  array_splice($lines, $input['insert_line'], 0, [preg_replace('/\n\z/', '', $input['insert_text'])]);
                  $store[$path] = implode("\n", $lines);
                  return "The file {$path} has been edited.";
              case 'delete':
                  if (!isset($store[$path])) {
                      return "Error: The path {$path} does not exist";
                  }
                  unset($store[$path]);
                  return "Successfully deleted {$path}";
              case 'rename':
                  if (!isset($store[$input['old_path']])) {
                      return "Error: The path {$input['old_path']} does not exist";
                  }
                  if (isset($store[$input['new_path']])) {
                      return "Error: The destination {$input['new_path']} already exists";
                  }
                  $store[$input['new_path']] = $store[$input['old


                  ---
title: Memory tool
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
description: Let Claude store and retrieve information across conversations by implementing the memory tool's file operations in your application.
---

The memory tool lets Claude store and retrieve information across conversations in a directory of memory files. Claude can create, read, update, and delete files that persist between sessions, building up knowledge over time without keeping everything in the context window.

Memory supports just-in-time context retrieval. Rather than loading all relevant information up front, an agent records what it learns in memory files and reads them back on demand. This keeps the active context focused on the current task, which matters for long-running sessions that would otherwise overwhelm the context window. See [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) for the broader pattern.

The memory tool operates client-side: Claude requests file operations, and your application executes them. You control where and how the data is stored through your own infrastructure.

<Note>
  Reach out through the [feedback form](https://forms.gle/YXC2EKGMhjN1c4L88) to share your feedback on this feature.
</Note>

<Note>
  To learn how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

## Use cases

* Maintain project context across multiple agent sessions
* Apply lessons from past interactions, decisions, and feedback to new tasks
* Build up a knowledge base over time

## How it works

When the memory tool is enabled, Claude automatically checks its memory directory before starting a task. As it works, Claude stores what it learns in files under `/memories` and reads them back in later conversations to continue earlier work.

Because the memory tool is client-side, Claude only requests memory operations. Your application executes each request against storage you control and returns the result in a `tool_result` block (see [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)). The `/memories` path is a prefix that your handler maps onto real storage, such as a per-user directory or keys in a database. Memory lives entirely in your application. A later conversation continues from the same memory when it sends the same `tools` entry and your handler serves the same store. For security, restrict all memory operations to the `/memories` directory (see [Path traversal protection](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#path-traversal-protection)).

### Example: How memory tool calls work

A typical interaction looks like this:

**1. User request:**

```text wrap
"Help me respond to this customer service ticket."
```

**2. Claude checks the memory directory:**

```text wrap
"I'll help you respond to the customer service ticket. Let me check my memory for any previous context."
```

Claude calls the memory tool:

```json
{
  "type": "tool_use",
  "id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "name": "memory",
  "input": {
    "command": "view",
    "path": "/memories"
  }
}
```

**3. Your application returns the directory contents:**

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "content": "Here're the files and directories up to 2 levels deep in /memories, excluding hidden items and node_modules:\n4.0K\t/memories\n1.5K\t/memories/customer_service_guidelines.xml\n2.0K\t/memories/refund_policies.xml"
}
```

**4. Claude reads relevant files:**

```json
{
  "type": "tool_use",
  "id": "toolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "name": "memory",
  "input": {
    "command": "view",
    "path": "/memories/customer_service_guidelines.xml"
  }
}
```

**5. Your application returns the file contents:**

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01D5E6F7G8H9I0J1K2L3M4N5",
  "content": "Here's the content of /memories/customer_service_guidelines.xml with line numbers:\n     1\t<guidelines>\n     2\t<addressing_customers>\n     3\t- Always address customers by their first name\n     4\t- Use empathetic language\n..."
}
```

**6. Claude uses the memory to help:**

```text wrap
"Based on your customer service guidelines, I can help you craft a response. Please share the ticket details..."
```

The memory tool is available on all Claude 4 and later models. For the full list of Anthropic-provided tools, see the [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference).

## Getting started

Using the memory tool takes two steps:

1. Add the memory tool to your request. The `tools` entry `{"type": "memory_20250818", "name": "memory"}` is the entire configuration: the `name` must be `memory`, and you don't define an input schema for an Anthropic-provided tool.
2. Implement a client-side handler for each memory command. Your handler must reject paths outside `/memories`, so read [Path traversal protection](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#path-traversal-protection) before you write it.

## Basic usage

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 2048,
      "messages": [
        {
          "role": "user",
          "content": "Help me respond to this customer service ticket."
        }
      ],
      "tools": [{
        "type": "memory_20250818",
        "name": "memory"
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 2048
  tools:
    - type: memory_20250818
      name: memory
  messages:
    - role: user
      content: Help me respond to this customer service ticket.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=2048,
      messages=[
          {
              "role": "user",
              "content": "Help me respond to this customer service ticket.",
          }
      ],
      tools=[{"type": "memory_20250818", "name": "memory"}],
  )

  print(message)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const message = await anthropic.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "Help me respond to this customer service ticket."
      }
    ],
    tools: [{ type: "memory_20250818", name: "memory" }]
  });

  console.log(message);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var message = await client.Messages.Create(
      new()
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 2048,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Help me respond to this customer service ticket.",
              },
          ],
          Tools = [new MemoryTool20250818()],
      }
  );

  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 2048,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Help me respond to this customer service ticket.")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfMemoryTool20250818: &anthropic.MemoryTool20250818Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.models.messages.MemoryTool20250818;
  // ...
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(2048L)
      .addTool(MemoryTool20250818.builder().build())
      .addUserMessage("Help me respond to this customer service ticket.")
      .build();

    Message message = client.messages().create(params);
    IO.println(message);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 2048,
      messages: [
          [
              'role' => 'user',
              'content' => 'Help me respond to this customer service ticket.',
          ],
      ],
      tools: [new MemoryTool20250818],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 2048,
    messages: [
      {
        role: "user",
        content: "Help me respond to this customer service ticket."
      }
    ],
    tools: [
      {
        type: "memory_20250818",
        name: "memory"
      }
    ]
  )
  puts message
  ```
</CodeGroup>

## Implement the memory handler

Claude's reply to a request like the previous one ends with a `tool_use` block that requests a memory operation, such as `view /memories`. Your application executes the operation and returns the result in a `tool_result` block, then sends the conversation back so Claude can continue: the standard [tool-use loop](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

Four SDKs provide memory tool helpers that handle the tool interface and the loop. Subclass `BetaAbstractMemoryTool` (Python and C#), use `betaMemoryTool` (TypeScript), or implement `BetaMemoryToolHandler` (Java) to back memory with your own storage, such as files on disk, a database, cloud storage, or encrypted files. Python and TypeScript also ship a ready-made local-filesystem implementation, `BetaLocalFilesystemMemoryTool`. The helper and tool-runner surfaces live in your SDK's beta namespace even though the memory tool itself doesn't require a beta header. The Go and Ruby SDKs have no memory helper, so those examples run the tool-use loop themselves, and PHP wraps your handler closure in its generic `BetaRunnableTool`. All three use an in-memory store that you replace with your own storage.

<CodeGroup exclude="shell">
  ```python Python
  import anthropic
  from anthropic.tools import BetaLocalFilesystemMemoryTool

  client = anthropic.Anthropic()
  memory = BetaLocalFilesystemMemoryTool(base_path="./memory")

  runner = client.beta.messages.tool_runner(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Remember that customer Acme Corp prefers email follow-ups.",
          }
      ],
      tools=[memory],
  )

  final_message = runner.until_done()
  print(final_message.content)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { betaMemoryTool } from "@anthropic-ai/sdk/helpers/beta/memory";
  import { BetaLocalFilesystemMemoryTool } from "@anthropic-ai/sdk/tools/memory/node";

  const client = new Anthropic();

  const backend = await BetaLocalFilesystemMemoryTool.init("./memory");
  const memory = betaMemoryTool(backend); // or pass your own handlers object

  const runner = client.beta.messages.toolRunner({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Remember that customer Acme Corp prefers email follow-ups."
      }
    ],
    tools: [memory],
    max_iterations: 10
  });

  const finalMessage = await runner;
  console.log(finalMessage.content);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Helpers.Beta;
  using Anthropic.Models.Beta.Messages;

  var client = new AnthropicClient();

  // Your subclass of BetaAbstractMemoryTool
  var memory = new FilesystemMemoryTool("./memories");

  var runner = client.Beta.Messages.ToolRunner(
      new MessageCreateParams
      {
          Model = Anthropic.Models.Messages.Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Remember that customer Acme Corp prefers email follow-ups.",
              },
          ],
      },
      [memory],
      maxIterations: 10
  );

  var finalMessage = await runner.RunUntilDoneAsync();
  Console.WriteLine(finalMessage);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"
  	"slices"
  	"sort"
  	"strings"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  // An in-memory store that maps memory file paths to their contents.
  // Use your own storage in production.
  var store = map[string]string{}

  type memoryCommand struct {
  	Command    string `json:"command"`
  	Path       string `json:"path"`
  	FileText   string `json:"file_text"`
  	OldStr     string `json:"old_str"`
  	NewStr     string `json:"new_str"`
  	InsertLine int    `json:"insert_line"`
  	InsertText string `json:"insert_text"`
  	OldPath    string `json:"old_path"`
  	NewPath    string `json:"new_path"`
  }

  func executeMemory(raw json.RawMessage) string {
  	var cmd memoryCommand
  	if err := json.Unmarshal(raw, &cmd); err != nil {
  		return "Error: invalid memory command"
  	}
  	switch cmd.Command {
  	case "view":
  		if content, ok := store[cmd.Path]; ok {
  			lines := strings.Split(strings.TrimSuffix(content, "\n"), "\n")
  			for i, line := range lines {
  				lines[i] = fmt.Sprintf("%6d\t%s", i+1, line)
  			}
  			return fmt.Sprintf("Here's the content of %s with line numbers:\n%s", cmd.Path, strings.Join(lines, "\n"))
  		}
  		if cmd.Path == "/memories" {
  			listing := []string{"1.0K\t/memories"}
  			for path := range store {
  				listing = append(listing, "1.0K\t"+path)
  			}
  			sort.Strings(listing[1:])
  			return fmt.Sprintf("Here're the files and directories up to 2 levels deep in %s, excluding hidden items and node_modules:\n%s", cmd.Path, strings.Join(listing, "\n"))
  		}
  		return fmt.Sprintf("The path %s does not exist. Please provide a valid path.", cmd.Path)
  	case "create":
  		store[cmd.Path] = cmd.FileText
  		return "File created successfully at: " + cmd.Path
  	case "str_replace":
  		content, ok := store[cmd.Path]
  		if !ok || !strings.Contains(content, cmd.OldStr) {
  			return fmt.Sprintf("No replacement was performed, old_str `%s` did not appear verbatim in %s.", cmd.OldStr, cmd.Path)
  		}
  		store[cmd.Path] = strings.Replace(content, cmd.OldStr, cmd.NewStr, 1)
  		return "The memory file has been edited."
  	case "insert":
  		content, ok := store[cmd.Path]
  		if !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.Path)
  		}
  		lines := strings.Split(content, "\n")
  		if cmd.InsertLine < 0 || cmd.InsertLine > len(lines) {
  			return fmt.Sprintf("Error: Invalid `insert_line` parameter: %d. It should be within the range of lines of the file: [0, %d]", cmd.InsertLine, len(lines))
  		}
  		lines = slices.Insert(lines, cmd.InsertLine, strings.TrimSuffix(cmd.InsertText, "\n"))
  		store[cmd.Path] = strings.Join(lines, "\n")
  		return fmt.Sprintf("The file %s has been edited.", cmd.Path)
  	case "delete":
  		if _, ok := store[cmd.Path]; !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.Path)
  		}
  		delete(store, cmd.Path)
  		return "Successfully deleted " + cmd.Path
  	case "rename":
  		if _, ok := store[cmd.OldPath]; !ok {
  			return fmt.Sprintf("Error: The path %s does not exist", cmd.OldPath)
  		}
  		if _, ok := store[cmd.NewPath]; ok {
  			return fmt.Sprintf("Error: The destination %s already exists", cmd.NewPath)
  		}
  		store[cmd.NewPath] = store[cmd.OldPath]
  		delete(store, cmd.OldPath)
  		return fmt.Sprintf("Successfully renamed %s to %s", cmd.OldPath, cmd.NewPath)
  	default:
  		return "Error: unknown command " + cmd.Command
  	}
  }

  func main() {
  	client := anthropic.NewClient()
  	tools := []anthropic.ToolUnionParam{{OfMemoryTool20250818: &anthropic.MemoryTool20250818Param{}}}
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Remember that customer Acme Corp prefers email follow-ups.")),
  	}

  	for {
  		message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5_5,
  			MaxTokens: 1024,
  			Messages:  messages,
  			Tools:     tools,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		if message.StopReason != anthropic.StopReasonToolUse {
  			for _, block := range message.Content {
  				if block.Type == "text" {
  					fmt.Println(block.Text)
  				}
  			}
  			break
  		}
  		results := []anthropic.ContentBlockParamUnion{}
  		for _, block := range message.Content {
  			if block.Type == "tool_use" {
  				results = append(results, anthropic.NewToolResultBlock(block.ID, executeMemory(block.Input), false))
  			}
  		}
  		messages = append(messages, message.ToParam(), anthropic.NewUserMessage(results...))
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.helpers.BetaMemoryToolHandler;
  import com.anthropic.helpers.BetaToolRunner;
  import com.anthropic.models.beta.messages.BetaMemoryTool20250818;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.MessageCreateParams; // beta package, not models.messages
  import com.anthropic.models.beta.messages.ToolRunnerCreateParams;
  import com.anthropic.models.messages.Model;
  import java.nio.file.Path;

  void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Your BetaMemoryToolHandler implementation of the six memory commands
    BetaMemoryToolHandler handler = new FileSystemMemoryToolHandler(Path.of("memories"));

    MessageCreateParams createParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .addTool(BetaMemoryTool20250818.builder().build())
      .addUserMessage("Remember that customer Acme Corp prefers email follow-ups.")
      .build();

    ToolRunnerCreateParams runnerParams = ToolRunnerCreateParams.builder()
      .betaMemoryToolHandler(handler)
      .initialMessageParams(createParams)
      .maxIterations(10)
      .build();

    BetaToolRunner runner = client.beta().messages().toolRunner(runnerParams);
    for (BetaMessage message : runner) {
      IO.println(message);
    }
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Beta\Messages\BetaMemoryTool20250818;
  use Anthropic\Client;
  use Anthropic\Lib\Tools\BetaRunnableTool;
  use Anthropic\Messages\Model;

  $client = new Client();

  // An in-memory store that maps memory file paths to their contents.
  // Use your own storage in production.
  $store = [];

  $memory = new BetaRunnableTool(
      definition: new BetaMemoryTool20250818,
      run: function (array $input) use (&$store): string {
          $path = $input['path'] ?? '';
          switch ($input['command']) {
              case 'view':
                  if (isset($store[$path])) {
                      $numbered = [];
                      foreach (explode("\n", preg_replace('/\n\z/', '', $store[$path])) as $i => $line) {
                          $numbered[] = sprintf("%6d\t%s", $i + 1, $line);
                      }
                      return "Here's the content of {$path} with line numbers:\n" . implode("\n", $numbered);
                  }
                  if ($path === '/memories') {
                      $listing = ["1.0K\t/memories"];
                      foreach (array_keys($store) as $stored) {
                          $listing[] = "1.0K\t{$stored}";
                      }
                      return "Here're the files and directories up to 2 levels deep in {$path}, excluding hidden items and node_modules:\n" . implode("\n", $listing);
                  }
                  return "The path {$path} does not exist. Please provide a valid path.";
              case 'create':
                  $store[$path] = $input['file_text'];
                  return "File created successfully at: {$path}";
              case 'str_replace':
                  $position = strpos($store[$path] ?? '', $input['old_str']);
                  if ($position === false) {
                      return "No replacement was performed, old_str `{$input['old_str']}` did not appear verbatim in {$path}.";
                  }
                  $store[$path] = substr_replace($store[$path], $input['new_str'] ?? '', $position, strlen($input['old_str']));
                  return 'The memory file has been edited.';
              case 'insert':
                  if (!isset($store[$path])) {
                      return "Error: The path {$path} does not exist";
                  }
                  $lines = explode("\n", $store[$path]);
                  if ($input['insert_line'] < 0 || $input['insert_line'] > count($lines)) {
                      return "Error: Invalid `insert_line` parameter: {$input['insert_line']}. It should be within the range of lines of the file: [0, " . count($lines) . "]";
                  }
                  array_splice($lines, $input['insert_line'], 0, [preg_replace('/\n\z/', '', $input['insert_text'])]);
                  $store[$path] = implode("\n", $lines);
                  return "The file {$path} has been edited.";
              case 'delete':
                  if (!isset($store[$path])) {
                      return "Error: The path {$path} does not exist";
                  }
                  unset($store[$path]);
                  return "Successfully deleted {$path}";
              case 'rename':
                  if (!isset($store[$input['old_path']])) {
                      return "Error: The path {$input['old_path']} does not exist";
                  }
                  if (isset($store[$input['new_path']])) {
                      return "Error: The destination {$input['new_path']} already exists";
                  }
                  $store[$input['new_path']] = $store[$input['old