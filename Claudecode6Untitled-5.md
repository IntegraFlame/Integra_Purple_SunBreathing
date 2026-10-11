---
title: Claude on Google Cloud
url: https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai
description: Anthropic's Claude models are available through [Google Cloud's Agent Platform](https://cloud.google.com/vertex-ai).
---

The API for accessing Claude on Google Cloud's Agent Platform is nearly identical to the [Messages API](https://platform.claude.com/docs/en/api/messages/create), with two key differences in request format:

* On Agent Platform, `model` is not passed in the request body. Instead, it is specified in the Google Cloud endpoint URL.
* On Agent Platform, `anthropic_version` is passed in the request body (rather than as a header), and must be set to the value `vertex-2023-10-16`.

Agent Platform is also supported by Anthropic's official [client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview). This guide walks you through making a request to Claude on Agent Platform using one of Anthropic's client SDKs.

Note that this guide assumes you already have a Google Cloud project that is able to use Agent Platform. See [Anthropic Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) for more information on the setup required and a full walkthrough.

## Install an SDK for accessing Agent Platform

First, install Anthropic's [client SDK](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) for your language of choice.

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic[vertex]"
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/vertex-sdk
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.Vertex
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go
    ```
  </Tab>

  <Tab title="Java">
    <CodeGroup exclude="shell, python, typescript, csharp, go, php, ruby">
      ```groovy Gradle
      implementation("com.anthropic:anthropic-java:2.69.0")
      implementation("com.anthropic:anthropic-java-vertex:2.69.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java</artifactId>
          <version>2.69.0</version>
      </dependency>
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-vertex</artifactId>
          <version>2.69.0</version>
      </dependency>
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Model;
      import com.anthropic.vertex.backends.VertexBackend;

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.builder()
              .backend(VertexBackend.fromEnv())
              .build();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .addUserMessage("What is the capital of France?")
              .build();

          Message response = client.messages().create(params);
          response.content().stream()
              .flatMap(block -> block.text().stream())
              .forEach(textBlock -> IO.println(textBlock.text()));
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk google/auth
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    # Gemfile
    gem "anthropic"
    gem "googleauth"
    ```
  </Tab>
</Tabs>

## Accessing Agent Platform

### Model availability

Note that Anthropic model availability varies by region. Search for "Claude" in the [Model Garden](https://cloud.google.com/model-garden) or go to [Anthropic Claude models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) for the latest information.

#### API model IDs

Lifecycle terms (Deprecated, Retired) are defined in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations). Lifecycle dates on partner-operated platforms are set by the partner and can differ from the Claude API schedule. For the current retirement date of any model on Agent Platform, see [Google Cloud's documentation for Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude).

| Model                                                                                                 | Agent Platform API model ID  |
| :---------------------------------------------------------------------------------------------------- | :--------------------------- |
| Claude Fable 5.1                                                                                      | `claude-fable-5-1`           |
| Claude Mythos 5.1 ([limited availability](https://support.claude.com/en/articles/14604842))           | `claude-mythos-5-1`          |
| Claude Fable 5                                                                                        | `claude-fable-5`             |
| Claude Mythos 5 ([limited availability](https://support.claude.com/en/articles/14604842))             | `claude-mythos-5`            |
| Claude Opus 5.5                                                                                       | `claude-opus-5-5`            |
| Claude Opus 5                                                                                         | `claude-opus-5`              |
| Claude Opus 4.8                                                                                       | `claude-opus-4-8`            |
| Claude Opus 4.7                                                                                       | `claude-opus-4-7`            |
| Claude Opus 4.6                                                                                       | `claude-opus-4-6`            |
| Claude Opus 4.5                                                                                       | `claude-opus-4-5@20251101`   |
| Claude Opus 4.1 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations))   | `claude-opus-4-1@20250805`   |
| Claude Opus 4 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations))     | `claude-opus-4@20250514`     |
| Claude Sonnet 5.5                                                                                     | `claude-sonnet-5-5`          |
| Claude Sonnet 5                                                                                       | `claude-sonnet-5`            |
| Claude Sonnet 4.6                                                                                     | `claude-sonnet-4-6`          |
| Claude Sonnet 4.5 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations)) | `claude-sonnet-4-5@20250929` |
| Claude Sonnet 4 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations))   | `claude-sonnet-4@20250514`   |
| Claude Haiku 5.5                                                                                      | `claude-haiku-5-5`           |
| Claude Haiku 4.5                                                                                      | `claude-haiku-4-5@20251001`  |
| Claude Haiku 3.5 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations))  | `claude-3-5-haiku@20241022`  |

<Tip>
  Upgrading to a newer Claude model? In Claude Code, run `/claude-api migrate` to apply model ID swaps and breaking parameter changes across your codebase. The skill detects which cloud platform your code targets and adjusts model ID formats and feature changes for that platform. See [Migrating to a newer Claude model](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

### Making requests

Before running requests you might need to run `gcloud auth application-default login` to authenticate with Google Cloud.

The following examples show how to generate text from Claude on Agent Platform:

<CodeGroup>
  ```bash cURL
  MODEL_ID=claude-opus-5-5
  PROJECT_ID=MY_PROJECT_ID

  curl https://aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/global/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "global";

  // Goes through the standard `google-auth-library` flow.
  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Uses default Google Cloud credentials
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Uses default Google Cloud credentials
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(VertexBackend.fromEnv())
          .build();

      Message message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      region: 'global',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-5-5',
  );
  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

See the [client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) and the official [Agent Platform docs](https://cloud.google.com/vertex-ai/docs) for more details.

Claude is also available through [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry).

## Data retention

Data handling for this offering is governed by Google Cloud. For details, see [Agent Platform and zero data retention](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance).

## Activity logging

Agent Platform provides a [request-response logging service](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging) that allows you to log the prompts and completions associated with your usage.

Anthropic recommends that you log your activity on at least a 30-day rolling basis to understand your activity and investigate any potential misuse.

<Note>
  Turning on this service does not give Google or Anthropic any access to your content.
</Note>

## Feature support

For the full feature list with Google Cloud availability, see [Features overview](https://platform.claude.com/docs/en/build-with-claude/overview).

### Supported feature highlights

* [Messages API](https://platform.claude.com/docs/en/api/messages/create)
* [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
* [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
* [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), including the [Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool), [Browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool), [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool), and [Text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool)
* [Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
* [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
* [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

### Features not supported

* Input sources (URL sources for images and documents, Files API)
* Server-side tools (code execution, web fetch, advisor)
* Agent infrastructure (Agent Skills, MCP connector, programmatic tool calling)
* API endpoints (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Server-side fallback (the [`fallbacks` parameter](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback); use the [client-side fallback pattern](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) instead)

### Context window

Claude Fable 5.1, Claude Fable 5, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, and Claude Haiku 5.5 have a [1M-token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) on Agent Platform. Other Claude models, including Sonnet 4.5 (deprecated) and Sonnet 4 (deprecated), have a 200k-token context window.

Agent Platform limits request payloads to 30 MB. When sending large documents or many images, you might reach this limit before the token limit.

## Global, multi-region, and regional endpoints

Agent Platform offers three endpoint types:

* **Global endpoints:** Dynamic routing for maximum availability
* **Multi-region endpoints:** Dynamic routing within a geographic area (for example, the United States or the European Union) for data residency with high availability
* **Regional endpoints:** Guaranteed data routing through specific geographic regions

Regional and multi-region endpoints include a 10% pricing premium over global endpoints.

<Note>
  This applies to Claude Sonnet 4.5 (deprecated) and future models only. Older models (Claude Sonnet 4 (deprecated), Opus 4 (deprecated), and earlier) maintain their existing pricing structures.
</Note>

### When to use each option

**Global endpoints (recommended):**

* Provide maximum availability and uptime
* Dynamically route requests to regions with available capacity
* No pricing premium
* Best for applications where data residency is flexible
* Only supports pay-as-you-go traffic (provisioned throughput requires regional endpoints)

**Multi-region endpoints:**

* Dynamically route requests across regions within a geographic area (currently `us` and `eu`)
* Useful when you need data residency within a broad geography but want higher availability than a single region
* 10% pricing premium over global endpoints
* Only supports pay-as-you-go traffic (provisioned throughput requires regional endpoints)

**Regional endpoints:**

* Route traffic through specific geographic regions
* Required for single-region data residency, strict compliance mandates, or provisioned throughput
* Support both pay-as-you-go and provisioned throughput
* 10% pricing premium reflects infrastructure costs for dedicated regional capacity

### Implementation

**Using global endpoints (recommended):**

Set the `region` parameter to `"global"` when initializing the client:

<CodeGroup>
  ```bash cURL
  MODEL_ID=claude-opus-5-5
  PROJECT_ID=MY_PROJECT_ID

  curl https://aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/global/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "global";

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Uses default Google Cloud credentials
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      // Uses default Google Cloud credentials
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("global")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      region: 'global',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-5-5',
  );

  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

**Using multi-region endpoints:**

Set the `region` parameter to a multi-region identifier: `"us"` for the United States or `"eu"` for the European Union. The SDK routes requests to the corresponding multi-region endpoint (`https://aiplatform.us.rep.googleapis.com` or `https://aiplatform.eu.rep.googleapis.com`), which dynamically balances traffic across regions within that geography.

<CodeGroup>
  ```bash cURL
  MODEL_ID=claude-opus-5-5
  LOCATION=us # Multi-region identifier: "us" or "eu"
  PROJECT_ID=MY_PROJECT_ID

  curl https://aiplatform.${LOCATION}.rep.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us"  # Multi-region identifier: "us" or "eu"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "us"; // Multi-region identifier: "us" or "eu"

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "us"; // Multi-region identifier: "us" or "eu"

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Multi-region identifier: "us" or "eu"
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      // Multi-region identifier: "us" or "eu"
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("us")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      region: 'us', // Multi-region identifier: "us" or "eu"
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-5-5',
  );
  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us", # Multi-region identifier: "us" or "eu"
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

**Using regional endpoints:**

Specify a specific region such as `"us-east5"` or `"europe-west1"`:

<CodeGroup>
  ```bash cURL
  # Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
  MODEL_ID=claude-sonnet-4-6
  LOCATION=us-east5 # Specify a specific region
  PROJECT_ID=MY_PROJECT_ID

  curl https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us-east5"  # Specify a specific region

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      # Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
      model="claude-sonnet-4-6",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "us-east5"; // Specify a specific region

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
    model: "claude-sonnet-4-6",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "us-east5"; // Specify a specific region

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Specify a specific region
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us-east5", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		// Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
  		Model:     anthropic.ModelClaudeSonnet4_6,
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      // Uses default Google Cloud credentials with specific region
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("us-east5") // Specify a specific region
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
                  .model(Model.CLAUDE_SONNET_4_6)
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      region: 'us-east5',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
      model: 'claude-sonnet-4-6',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us-east5", # Specify a specific region
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    # Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
    model: "claude-sonnet-4-6",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

<Note>
  Claude Mythos Preview is a research preview available to invited customers on Agent Platform. For more information, see [Project Glasswing](https://anthropic.com/glasswing).
</Note>

## Additional resources

* **Agent Platform pricing:** [Generative AI pricing on cloud.google.com](https://cloud.google.com/vertex-ai/generative-ai/pricing)
* **Claude models documentation:** [Claude on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude)
* **Google blog post:** [Global endpoint for Claude models](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)
* **Anthropic pricing details:** [Cloud platform pricing](https://platform.claude.com/docs/en/about-claude/pricing#cloud-platform-pricing)

---
title: Browser and computer use with the SDK toolsets
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk
description: Run the browser use tool or the computer use tool from the Python or TypeScript SDK. The SDK runs the loop and the checks you configure, and you supply the browser or the desktop.
---

The Python and TypeScript SDKs include a class for the [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) and a class for the [computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool). You subclass one and write one method per member tool, such as `navigate` or `left_click`, against your own browser or desktop automation. The SDK routes each call, runs the policies you pass, asks your approval callback, and builds each `tool_result`.

Most of this page uses the browser class. [Computer toolset](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#computer-toolset) covers the computer class and what differs for it.

The SDK doesn't include a browser, a desktop, a ready-made driver, or a URL policy. The [minimal CDP example](https://github.com/anthropics/claude-quickstarts/tree/main/browser-toolset) is in the claude-quickstarts repository, in Python and TypeScript. It controls Chromium through the Chrome DevTools Protocol (CDP), and it isn't production code.

<Note>
  The browser toolset class is in beta and available in the [Python SDK](https://github.com/anthropics/anthropic-sdk-python/blob/main/browser-toolset.md) and the [TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/browser-toolset.md). The computer toolset class is in beta in the same SDKs, which have a [Python computer toolset guide](https://github.com/anthropics/anthropic-sdk-python/blob/main/computer-toolset.md) and a [TypeScript computer toolset guide](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/computer-toolset.md). Each class runs with the [tool runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) or in a loop you write.
</Note>

## Partner integrations

Browser Use, Browserbase, Daytona, and E2B publish their own integrations with the SDK toolsets.

### Browser Use

* [Browser Use docs](https://docs.browser-use.com/open-source/customize/integrations/toolsets-for-claude)
* [Browser Use quickstart](https://github.com/browser-use/browser-use/tree/main/examples/integrations/toolsets-for-claude)

### Browserbase

* [Browserbase Stagehand docs](https://docs.stagehand.dev/v4/integrations/agent-frameworks/claude-cua-toolset-quickstart)
* [Browserbase toolset](https://github.com/browserbase/claude-cua-toolset)

### Daytona

* [Daytona guide](https://www.daytona.io/docs/en/guides/claude/claude-draws-daytona-sandbox/)

### E2B

* [E2B docs](https://docs.e2b.dev/agents/claude-toolsets)
* [E2B example](https://github.com/e2b-dev/e2b-cookbook/tree/main/examples/anthropic-computer-use-orangehrm-js)

## Quick start

A driver is your subclass of `BetaAbstractBrowserToolset20260801`. This one implements `navigate`, `screenshot`, and `left_click`, plus `_browser_state` (typescript: `browserState`), the state report that every driver needs. In the example, `backend` stands for your own wrapper around a browser automation library, such as Playwright. The URL policy is an example. [Write a URL policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy) explains it.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import re
  from urllib.parse import urlsplit

  from anthropic import Anthropic
  from anthropic.tools import ToolError
  from anthropic.tools.browser import (
      BetaAbstractBrowserToolset20260801,
      BetaBrowserNavigateResult,
      BetaBrowserState,
      BetaScreenshotResult,
      BetaToolsetCallContext,
      BetaURLContext,
  )
  from anthropic.types.beta import (
      BetaBrowserLeftClickInput,
      BetaBrowserNavigateInput,
      BetaBrowserScreenshotInput,
      BetaBrowserStateTabEntryParam,
  )


  class MyBrowser(BetaAbstractBrowserToolset20260801):
      def __init__(self, backend, **options):
          super().__init__(**options)
          self.backend = backend

      def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
          return BetaBrowserState(
              tabs=[
                  BetaBrowserStateTabEntryParam(
                      tab_id=tab.id,
                      title=tab.title,
                      url=tab.url,
                      active=tab.id == self.backend.active,
                  )
                  for tab in self.backend.tabs()
              ],
              state_changes=self.backend.drain_changes(),
          )

      def navigate(
          self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
      ) -> BetaBrowserNavigateResult:
          # input.url is "back", "forward", "reload", or a URL that your URL policy
          # allowed, as Claude wrote it. Like is_allowed, backend.goto adds https://
          # to a URL that doesn't start with a scheme.
          page = self.backend.goto(input.url, input.tab_id)
          return BetaBrowserNavigateResult(
              url=page.url, status=page.status, title=page.title
          )

      def screenshot(
          self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput
      ) -> BetaScreenshotResult:
          data = self.backend.png_base64(input.tab_id)
          return BetaScreenshotResult(data=data, media_type="image/png")

      def left_click(
          self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickInput
      ) -> None:
          # Nothing to return: Claude reads "Clicked."
          self.backend.click(input.target, input.tab_id)

      def close(self) -> None:
          super().close()  # first, so no call is still using the browser when it closes
          if not self.backend.closed:
              self.backend.close()


  ALLOWED_HOSTS = ("example.com", "iana.org")
  SCHEME_PREFIX = re.compile(r"[a-z][a-z0-9+.-]*:", re.IGNORECASE)


  def is_allowed(url: str) -> bool:
      # An example, not a production policy. See "Write a URL policy".
      if url.lower() == "about:blank":
          return True
      with_scheme = url if SCHEME_PREFIX.match(url) else f"https://{url}"
      # A browser reads "\" as "/" in a web URL.
      try:
          parts = urlsplit(with_scheme.replace("\\", "/"))
      except ValueError:
          return False
      host = parts.hostname or ""
      listed = any(host == name or host.endswith(f".{name}") for name in ALLOWED_HOSTS)
      return parts.scheme in ("http", "https") and listed


  def url_policy(context: BetaURLContext, url: str) -> None:
      if not is_allowed(url):
          raise ToolError(f"blocked: {url} is not on an allowed host")


  client = Anthropic()
  with MyBrowser(backend, url_policy=url_policy) as browser:
      runner = client.beta.messages.tool_runner(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=[browser],
          messages=[
              {
                  "role": "user",
                  "content": "Open example.com and tell me the page heading.",
              }
          ],
          stream=True,
          run_tools_eagerly=True,  # so a call can start before the response ends
      )
      for stream in runner:
          print(stream.get_final_message())
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import {
    BetaAbstractBrowserToolset20260801,
    type BetaBrowserNavigateResult,
    type BetaBrowserToolsetOptions,
    type BetaScreenshotResult,
    type BetaToolsetCallContext,
    type BetaURLContext,
    ToolError
  } from "@anthropic-ai/sdk/helpers/beta/toolsets";
  import type {
    BetaBrowserLeftClickInput,
    BetaBrowserNavigateInput,
    BetaBrowserScreenshotInput
  } from "@anthropic-ai/sdk/resources/beta";

  class MyBrowser extends BetaAbstractBrowserToolset20260801 {
    constructor(
      private backend: Backend,
      options: Omit<BetaBrowserToolsetOptions, "browserState"> = {}
    ) {
      super({
        ...options,
        // Required: every open tab, and what changed since the last report.
        browserState: () => ({
          tabs: backend.tabs().map((tab) => ({
            tab_id: tab.id,
            title: tab.title,
            url: tab.url,
            active: tab.id === backend.active
          })),
          state_changes: backend.drainChanges()
        })
      });
    }

    protected override async navigate(
      ctx: BetaToolsetCallContext,
      input: BetaBrowserNavigateInput
    ): Promise<BetaBrowserNavigateResult> {
      // input.url is "back", "forward", "reload", or a URL that your URL policy
      // allowed, as Claude wrote it. Like isAllowed, backend.goto adds https:// to
      // a URL that doesn't start with a scheme.
      const page = await this.backend.goto(input.url, input.tab_id);
      return { url: page.url, status: page.status, title: page.title };
    }

    protected override async screenshot(
      ctx: BetaToolsetCallContext,
      input: BetaBrowserScreenshotInput
    ): Promise<BetaScreenshotResult> {
      return { data: await this.backend.pngBase64(input.tab_id), mediaType: "image/png" };
    }

    protected override async left_click(
      ctx: BetaToolsetCallContext,
      input: BetaBrowserLeftClickInput
    ): Promise<void> {
      // Nothing to return: Claude reads "Clicked."
      await this.backend.click(input.target, input.tab_id);
    }

    override async close(): Promise<void> {
      await super.close(); // first, so no call is still using the browser when it closes
      if (!this.backend.closed) await this.backend.close();
    }
  }

  const ALLOWED_HOSTS = ["example.com", "iana.org"];
  const SCHEME_PREFIX = /^[a-z][a-z0-9+.-]*:/i;

  // An example, not a production policy. See "Write a URL policy".
  function isAllowed(url: string): boolean {
    if (url.toLowerCase() === "about:blank") return true;
    const withScheme = SCHEME_PREFIX.test(url) ? url : `https://${url}`;
    // A browser reads "\" as "/" in a web URL.
    const parsed = URL.parse(withScheme.replaceAll("\\", "/"));
    const host = parsed?.hostname ?? "";
    const listed = ALLOWED_HOSTS.some((name) => host === name || host.endsWith(`.${name}`));
    return (parsed?.protocol === "http:" || parsed?.protocol === "https:") && listed;
  }

  function urlPolicy(ctx: BetaURLContext, url: string): void {
    if (!isAllowed(url)) throw new ToolError(`blocked: ${url} is not on an allowed host`);
  }

  const client = new Anthropic();
  const browser = new MyBrowser(backend, { urlPolicy });
  try {
    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: [browser],
      messages: [{ role: "user", content: "Open example.com and tell me the page heading." }],
      stream: true,
      runToolsEagerly: true // so a call can start before the response ends
    });
    for await (const stream of runner) console.log(await stream.finalMessage());
  } finally {
    await browser.close();
  }
  ```
</CodeGroup>

Pass the driver instance itself as the `tools` entry. A member you don't implement is sent to the API as disabled. If Claude calls it anyway, the SDK returns an error, and the run continues. Overriding `execute` changes which members are sent as disabled ([Add before and after hooks](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#add-before-and-after-hooks)). The runner never closes the toolset, so one instance can serve several runs. Close it when you're done.

The example turns on early start. See [Start calls while the response streams](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#start-calls-while-the-response-streams).

<Warning>
  Do these two things before you run a driver against anything but a throwaway browser:

  * [Write a URL policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy), and block private network ranges and the cloud metadata address `169.254.169.254` with [egress rules on the container](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container). Without a URL policy, the SDK checks no URL. Egress rules outside the container don't see loopback, so a page can still reach anything listening in the browser's container.
  * Use a browser profile that isn't signed in to any account whose data or actions you wouldn't hand to Claude. See [Isolate the browser host](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#isolate-the-browser-host).
</Warning>

## Customize a driver

### Enable or disable members

`configs` takes the per-member settings described under [Configure the toolset](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#configure-the-toolset). List only the members you change:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  # A MyBrowser that also implements read_console
  browser = MyBrowser(
      backend, configs={"read_console": {"enabled": True}, "navigate": {"enabled": False}}
  )
  ```

  ```typescript TypeScript
  // A MyBrowser that also implements read_console
  const browser = new MyBrowser(backend, {
    configs: { read_console: { enabled: true }, navigate: { enabled: false } }
  });
  ```
</CodeGroup>

The SDK refuses a call to a disabled member before your code runs. Enabling a member your class doesn't implement is a configuration error, unless the class overrides `execute`.

### Add before and after hooks

Override `execute` and call the parent's `execute`. Code before that call runs after the [URL policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy), the [file policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads), and [`confirm`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#gate-consequential-members), and it can change the input. The SDK doesn't check the changed input again. Code after the call receives the result, and it can change the result. Raise `ToolError` (throw it in TypeScript) to refuse the call.

Overriding `execute` changes which members Claude is offered. The SDK counts every member as implemented, so Claude is offered every member that's on by default. The quick start's `MyBrowser` serves three members, so the following `TracedBrowser` offers Claude members it can't serve. Turn those members off with `configs` before you use it.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import time


  class TracedBrowser(MyBrowser):
      def execute(self, context, name, input):
          started = time.monotonic()
          result = super().execute(context, name, input)
          elapsed_ms = (time.monotonic() - started) * 1000
          call_id = context.tool_use.id if context.tool_use else "-"
          log.info("%s %s %.0fms", call_id, name, elapsed_ms)
          return redact(result) if name == "get_page_text" else result
  ```

  ```typescript TypeScript
  import type { BetaToolsetCallContext } from "@anthropic-ai/sdk/helpers/beta/toolsets";
  import type {
    BetaBrowserMemberInput,
    BetaBrowserMemberName
  } from "@anthropic-ai/sdk/resources/beta";

  class TracedBrowser extends MyBrowser {
    protected override async execute(
      ctx: BetaToolsetCallContext,
      name: BetaBrowserMemberName,
      input: BetaBrowserMemberInput
    ) {
      const started = performance.now();
      const result = await super.execute(ctx, name, input);
      log.info(`${ctx.toolUse?.id ?? "-"} ${name} ${Math.round(performance.now() - started)}ms`);
      return name === "get_page_text" ? redact(result as string) : result;
    }
  }
  ```
</CodeGroup>

## Implement a driver

Override the members your browser supports. Each member receives the call context and the member's input as a typed object, such as `BetaBrowserNavigateInput`. The input types come from `anthropic.types.beta` (typescript: `@anthropic-ai/sdk/resources/beta`). [Member tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#member-tools) lists each input's fields.

In TypeScript, write members as methods, not arrow-function fields, because the SDK finds them on the prototype. Spell the `type` member `type_` in TypeScript. In Python, it's `type`.

### Return results

What a member returns determines what Claude reads. A successful result ends with a `browser_state` block built from your state report. An error result carries no block.

| Member                                                                                  | Returns                                                                                              | Claude reads                                                                                |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `screenshot`, `zoom`                                                                    | `BetaScreenshotResult`                                                                               | One image block                                                                             |
| `navigate`                                                                              | `BetaBrowserNavigateResult`                                                                          | `Navigated to {url} — {title} (HTTP {status})`                                              |
| `new_tab`, `switch_tab`, `list_tabs`, `close_tab`                                       | A tab entry (`new_tab`, `switch_tab`), a list of tab entries (`list_tabs`), or nothing (`close_tab`) | The `browser_state` block alone                                                             |
| `read_page`, `get_page_text`, `find`, `read_console`, `read_network`, `javascript_exec` | A string                                                                                             | The string, or `(empty)` for an empty string                                                |
| Every other member                                                                      | Nothing, or one line of text                                                                         | A short confirmation, such as `Clicked.`, then the returned line in a text block of its own |

### Report browser state

The SDK calls `_browser_state` (typescript: `browserState`) after each call that returns a result, including refused and failed calls. Return every open tab, and what changed since the last report:

* Opened tabs and download events.
* A `BetaNavigationRefused` for each navigation your [request hook](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver) blocked.
* A `BetaDialogDismissed` for each native dialog your driver dismissed.

Put all of these in `state_changes`. In Python, `BetaNavigationRefused()` and `BetaDialogDismissed(kind=..., message=...)` come from `anthropic.tools.browser`. In TypeScript, they're `{ type: "navigation_refused" }` and `{ type: "dialog_dismissed", kind, message }`.

The last two aren't API state changes. The SDK reports them to Claude as text outside the `browser_state` block: one line for all refused navigations, which doesn't name a URL, and a line for each of the first three dismissed dialogs, then a count of any others.

When any tab is open, exactly one must be active. Every member that takes a `tab_id` must act on the tab it names. The API's limits on the report are listed under [Track tabs with `browser_state`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#track-tabs-and-page-state).

Claude reads each tab's URL, each download's URL, and the URL that your `navigate` returns, as your driver wrote them. The SDK doesn't parse these URLs. It turns line breaks and other control characters into spaces, trims the ends, and cuts each URL at 4,096 characters. So a `data:` URL's contents, a `file:` URL's path, and a user name or password in a URL all reach Claude.

### Handle errors

| Raised by a member or the SDK | Claude reads                                                                         | The run   |
| ----------------------------- | ------------------------------------------------------------------------------------ | --------- |
| `ToolError`                   | Its message, as an error result                                                      | Continues |
| `ToolsetUsageError`           | Nothing                                                                              | Stops     |
| Any other exception           | `ClassName: message` in Python or `Error: message` in TypeScript, as an error result | Continues |

The SDK raises `ToolsetUsageError` for a configuration error, a misuse of the SDK during a call, or a call after `close`. It also raises one when `_browser_state` (typescript: `browserState`) raises any exception, even a `ToolError`. The tool runner and `tool_result` (typescript: `toolResult`) don't catch it, so it reaches their caller.

The SDK doesn't hide local paths in a member's error text, in the line an action such as `left_click` returns, in a failed download's error, or in a dismissed dialog's message.

A `ToolError` from your URL policy, file policy, or `confirm` callable reaches Claude as written, so leave local paths out of its text. Catch exceptions in your members, and raise `ToolError` (throw it in TypeScript) with your own text.

### Start calls while the response streams

By default, the tool runner runs a turn's calls after Claude's response ends. With early start, it can start a browser or computer call while the response is still streaming.

To turn it on, pass `stream=True` (typescript: `stream: true`) and `run_tools_eagerly=True` (typescript: `runToolsEagerly: true`) to the tool runner, as the quick start does. With `stream`, each pass through your loop over the runner gives you a stream instead of a message.

Early start changes when a call can start, not how the toolset runs it:

* **The checks still run first:** The SDK calls your URL policy, your file policy, and `confirm` before a call runs. With early start, it can call `confirm` while the response is still streaming.
* **Calls still run one at a time:** A toolset runs its calls in the order Claude wrote them. A failed call still stops that toolset's later calls in the turn.
* **A call that has started can't be taken back:** If the response is then cut off, for example at `max_tokens`, or your loop stops early, the action still happens, and Claude never reads its result.

### Run without the tool runner

Pass the instance in `tools` (`browser.toJSON()` in TypeScript), and answer each member call with `tool_result` (typescript: `toolResult`). The browser use tool requires you to stop at the first failed call ([Batch actions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#batch-actions)). After a failed call, this loop answers the turn's later calls without running them:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.types.beta import BetaMessageParam, BetaToolResultBlockParam

  NOT_EXECUTED = "Not executed: an earlier action in this turn failed."
  MAX_TURNS = 10

  with MyBrowser(backend, url_policy=url_policy) as browser:
      messages: list[BetaMessageParam] = [{"role": "user", "content": "Open example.com"}]
      for _ in range(MAX_TURNS):
          response = client.beta.messages.create(
              model="claude-opus-5-5",
              max_tokens=1024,
              tools=[browser],
              messages=messages,
          )
          messages.append({"role": "assistant", "content": response.content})
          calls = [
              block
              for block in response.content
              if block.type == "tool_use" and block.toolset_name == browser.toolset_name
          ]
          if not calls:
              break
          results: list[BetaToolResultBlockParam] = []
          failed = False
          for call in calls:
              if failed:
                  # After a failed call, the rest of the turn is answered, not run.
                  results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": call.id,
                          "toolset_name": call.toolset_name,
                          "content": NOT_EXECUTED,
                          "is_error": True,
                      }
                  )
                  continue
              result = browser.tool_result(call)
              failed = bool(result.get("is_error"))
              results.append(result)
          messages.append({"role": "user", "content": results})
  ```

  ```typescript TypeScript
  const NOT_EXECUTED = "Not executed: an earlier action in this turn failed.";
  const MAX_TURNS = 10;

  const browser = new MyBrowser(backend, { urlPolicy });
  try {
    const messages: Anthropic.Beta.BetaMessageParam[] = [
      { role: "user", content: "Open example.com" }
    ];
    for (let turn = 0; turn < MAX_TURNS; turn++) {
      const response = await client.beta.messages.create({
        model: "claude-opus-5-5",
        max_tokens: 1024,
        tools: [browser.toJSON()],
        messages
      });
      messages.push({ role: "assistant", content: response.content });
      const calls = response.content.filter(
        (block): block is Anthropic.Beta.BetaToolUseBlock =>
          block.type === "tool_use" && block.toolset_name === browser.toolsetName
      );
      if (calls.length === 0) break;
      const results: Anthropic.Beta.BetaToolResultBlockParam[] = [];
      let failed = false;
      for (const call of calls) {
        if (failed) {
          // After a failed call, the rest of the turn is answered, not run.
          results.push({
            type: "tool_result",
            tool_use_id: call.id,
            toolset_name: call.toolset_name,
            content: NOT_EXECUTED,
            is_error: true
          });
          continue;
        }
        const result = await browser.toolResult(call);
        failed = result.is_error === true;
        results.push(result);
      }
      messages.push({ role: "user", content: results });
    }
  } finally {
    await browser.close();
  }
  ```
</CodeGroup>

Each answer to a skipped call carries `is_error`, the call's `toolset_name`, and the exact text that [Batch actions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#batch-actions) requires. The tool runner sends the same answer.

## Run the toolset safely

Claude's next action depends on the pages it reads. A page, or text injected into one, can try to reach internal services or pull files off the host. It can also try to trigger actions with real effects. Before you run a driver against anything but a throwaway browser, take these six steps:

1. [Write a URL policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy) that refuses every `navigate` URL the task doesn't need.
2. [Intercept requests in the driver](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver), and check each request with the same rules.
3. [Put egress policy on the container](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container), so the network blocks what the driver can't see.
4. [Confine uploads and downloads](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads), or leave uploads off.
5. [Gate consequential members](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#gate-consequential-members) with `confirm`.
6. [Isolate the browser host](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#isolate-the-browser-host) in a dedicated container or VM for each session.

The SDK applies steps 1, 4, and 5 through the policies and the callable you pass. Steps 2, 3, and 6 are up to your driver and your deployment. The precautions under [Security considerations](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#security-considerations) apply as well.

<Note>
  Anthropic's prompt-injection classifiers, described under [Security considerations](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#security-considerations), don't currently run on browser toolset requests sent through Amazon Bedrock.
</Note>

### Write a URL policy

<Warning>
  Without a URL policy, the SDK checks no URL, and the API doesn't filter the URLs Claude opens. Even with a policy, a link Claude clicks or a redirect can take the browser to loopback (`localhost`, `127.0.0.1`), to link-local addresses such as the cloud metadata address `169.254.169.254`, and to private network ranges. [Egress rules on the container](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container) can block the link-local and private addresses. Rules enforced outside the container can't block loopback.

  The SDK doesn't check a URL's scheme, so your driver must refuse every scheme it doesn't mean to open, such as `javascript:`, `view-source:`, `data:`, and `file:`. Most drivers need only `http` and `https`. The example policy below allows only `http` and `https` URLs, plus `about:blank`.

  A `file:` URL lets Claude read files on the browser host. A `javascript:` URL runs script in the current page, even when `javascript_exec` is off. Egress rules don't stop either one.
</Warning>

A URL policy is a function that you pass as `url_policy` (typescript: `urlPolicy`). You write the policy, and you're responsible for making it ready for production. Before your `navigate` runs, the SDK calls the policy with the call's context and the URL as Claude wrote it.

Return nothing to allow the URL. To refuse it, raise `ToolError` (throw it in TypeScript). Claude reads the error's message, and `navigate` doesn't run. The policy checks only the URL in each `navigate` call. It isn't a network control.

This is the policy from the quick start. It allows `about:blank`, plus two sites and their subdomains over `http` and `https`:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import re
  from urllib.parse import urlsplit

  from anthropic.tools import ToolError
  from anthropic.tools.browser import BetaURLContext

  ALLOWED_HOSTS = ("example.com", "iana.org")
  SCHEME_PREFIX = re.compile(r"[a-z][a-z0-9+.-]*:", re.IGNORECASE)


  def is_allowed(url: str) -> bool:
      # An example, not a production policy.
      if url.lower() == "about:blank":
          return True
      with_scheme = url if SCHEME_PREFIX.match(url) else f"https://{url}"
      # A browser reads "\" as "/" in a web URL.
      try:
          parts = urlsplit(with_scheme.replace("\\", "/"))
      except ValueError:
          return False
      host = parts.hostname or ""
      listed = any(host == name or host.endswith(f".{name}") for name in ALLOWED_HOSTS)
      return parts.scheme in ("http", "https") and listed


  def url_policy(context: BetaURLContext, url: str) -> None:
      if not is_allowed(url):
          raise ToolError(f"blocked: {url} is not on an allowed host")


  browser = MyBrowser(backend, url_policy=url_policy)
  ```

  ```typescript TypeScript
  import { type BetaURLContext, ToolError } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const ALLOWED_HOSTS = ["example.com", "iana.org"];
  const SCHEME_PREFIX = /^[a-z][a-z0-9+.-]*:/i;

  // An example, not a production policy.
  function isAllowed(url: string): boolean {
    if (url.toLowerCase() === "about:blank") return true;
    const withScheme = SCHEME_PREFIX.test(url) ? url : `https://${url}`;
    // A browser reads "\" as "/" in a web URL.
    const parsed = URL.parse(withScheme.replaceAll("\\", "/"));
    const host = parsed?.hostname ?? "";
    const listed = ALLOWED_HOSTS.some((name) => host === name || host.endsWith(`.${name}`));
    return (parsed?.protocol === "http:" || parsed?.protocol === "https:") && listed;
  }

  function urlPolicy(ctx: BetaURLContext, url: string): void {
    if (!isAllowed(url)) throw new ToolError(`blocked: ${url} is not on an allowed host`);
  }

  const browser = new MyBrowser(backend, { urlPolicy });
  ```
</CodeGroup>

The SDK calls the policy only for `navigate`, and not for `"back"`, `"forward"`, or `"reload"`. Claude can leave out the scheme, as in `example.com`, so before it reads the host, the example adds `https://` to a URL that doesn't start with a scheme. Your `navigate` gets the URL as Claude wrote it. Add the scheme there with the same test, so that the browser opens the URL your policy checked.

The example isn't production grade. A production policy needs much more, in areas such as these:

* Links Claude clicks, forms it submits, redirects, and the requests a page makes on its own. Only your driver sees them. See [Intercept requests in the driver](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver).
* Hostnames and URLs that come from page content, which an attacker can choose.
* Parsing each URL the way the browser does, not finding the hostname with a plain string split.
* URL schemes. The SDK doesn't check them, so refuse every scheme your driver doesn't mean to open.
* Egress rules on the container, for what no URL check can see. See [Put egress policy on the container](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container).

If you pass `url_policy=None` (typescript: `urlPolicy: null`), the SDK refuses every `navigate` to a URL, so a `None` (typescript: `null`) read from your configuration can't leave URLs unchecked by accident. In TypeScript, `undefined` leaves the option unset, the same as not passing it.

### Intercept requests in the driver

The URL policy judges only the URL in a `navigate` call. A link Claude clicks, a form it submits, a redirect, or an image or script on an allowed page can still reach a host the policy would refuse. Use [egress rules](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container) to block those hosts.

A driver with request interception can also check those requests in its request hook, the function your automation library calls before each request. Call the function that your policy uses, so that you write the rules once:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  class MyBrowser(BetaAbstractBrowserToolset20260801):
      ...

      # Registered on a Playwright browser context with context.route("**/*", self._guard)
      def _guard(self, route):
          # is_allowed is the function from "Write a URL policy"
          if not is_allowed(route.request.url):
              return route.abort("blockedbyclient")
          route.continue_()
  ```

  ```typescript TypeScript
  // In the driver class, on a Playwright browser context.
  // isAllowed is the function from "Write a URL policy".
  await context.route("**/*", (route) =>
    isAllowed(route.request().url()) ? route.continue() : route.abort("blockedbyclient")
  );
  ```
</CodeGroup>

A request hook like this one doesn't see WebSocket handshakes, service-worker requests, or redirect hops. Block service workers. Check WebSocket handshakes and redirect hops with a hook that sees them. The example policy refuses `ws://` and `wss://` URLs, so change `ws://` to `http://` and `wss://` to `https://` before you pass a WebSocket URL to `is_allowed` (typescript: `isAllowed`).

### Put egress policy on the container

Interception can't see every request the browser makes, and the URL policy doesn't see where a name resolves. An egress policy that the container's network enforces covers both:

* Block link-local and private address ranges in IPv4 and IPv6. That includes the cloud metadata address `169.254.169.254`.
* Allow outbound connections only to the hosts the task needs. If your rules match IP addresses, resolve the hostnames you allow when the container starts.
* Allow DNS only to the container's resolver.

Rules enforced outside the browser's container, such as a Kubernetes NetworkPolicy or a cloud firewall, don't see loopback inside it. With only those rules, a page can reach anything listening there, including a DevTools port, which shows a list of the browser's open tabs and the address that controls each one.

### Confine uploads and downloads

`file_upload` is off by default. With no `file_policy` (typescript: `filePolicy`), the SDK refuses every upload that names a path or a [document ID](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool#upload-files). To enable uploads, pass a `BetaLocalFilePolicy` (typescript: `BetaNodeFilePolicy`) with one upload directory that holds only the task's files:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.tools.browser import BetaLocalFilePolicy

  # A MyBrowser that also implements file_upload
  browser = MyBrowser(
      backend,
      configs={"file_upload": {"enabled": True}},
      confirm=make_confirm(),  # required for file_upload; see Gate consequential members
      url_policy=url_policy,
      file_policy=BetaLocalFilePolicy(
          upload_roots=["/task/uploads"],
          download_dir="/task/downloads",
          expose_download_paths=False,
      ),
  )
  ```

  ```typescript TypeScript
  import { BetaNodeFilePolicy } from "@anthropic-ai/sdk/helpers/beta/toolsets/node";

  // A MyBrowser that also implements file_upload
  const browser = new MyBrowser(backend, {
    configs: { file_upload: { enabled: true } },
    confirm: makeConfirm(), // required for file_upload; see Gate consequential members
    urlPolicy,
    filePolicy: new BetaNodeFilePolicy({
      uploadRoots: ["/task/uploads"],
      downloadDir: "/task/downloads",
      exposeDownloadPaths: false
    })
  });
  ```
</CodeGroup>

The SDK resolves each upload path, following symlinks, and refuses any path outside the upload roots. The file policy raises a configuration error for a download directory that is an upload root, is inside one, or contains one. That check can miss a symlink, so don't let one make the download directory the same as an upload root, or put one inside the other. The SDK includes a download's `path` in the state report only when `expose_download_paths` (typescript: `exposeDownloadPaths`) is true and the file is inside the download directory.

The shipped file policy checks paths on the filesystem of the process that runs the SDK. It protects only a browser that shares that filesystem. For a remote browser, follow [Remote and hosted browsers](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#remote-and-hosted-browsers) instead.

Set up downloads this way:

* Create the download directory yourself with mode `0700`, and mount it `noexec,nosuid,nodev`.
* Keep the directory out of reach of other tools that Claude can call, such as a shell or a file tool.
* In a `download_failed` state change, write `error` as a fixed phrase. An exception's text can contain the path or the URL.
* Don't read a downloaded file into the conversation, or run it, until a person decides to.

### Gate consequential members

`javascript_exec` and `file_upload` are off by default. If you enable either one without a `confirm` callable, the constructor raises a configuration error. With a `confirm` callable, the SDK calls it before every call that's about to run. Without one, nothing is asked. In TypeScript, `confirm: null` doesn't raise the configuration error, and the SDK refuses every call to any member.

Return `True` (typescript: `true`) to run the call, or `False` (typescript: `false`) to refuse it. When your callable asks a person, show them the member, the page's URL, and the call's input. First, escape every character outside printable ASCII in the URL and the input, because both can carry text from the page.

This example asks about the two gated members through your own `ask_user` (typescript: `askUser`) function, and approves the rest:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import json
  from collections.abc import Callable
  from urllib.parse import urlsplit

  from anthropic.tools.browser import BetaConfirmContext

  GATED = {"javascript_exec", "file_upload"}


  def shown(value: object) -> str:
      """A value as JSON, with every character outside printable ASCII escaped."""
      return json.dumps(value, ensure_ascii=True, indent=2)


  def make_confirm() -> Callable[[BetaConfirmContext], bool]:
      granted: set[tuple[str, str, str]] = set()

      def confirm(context: BetaConfirmContext) -> bool:
          name = context.member
          if name not in GATED:
              return True
          detail = shown(context.input.to_dict())
          page = context.tab_url
          where = shown(page) if page else "a tab with no URL"
          question = f"Allow {name} on {where}?\n{detail}"
          if page is None or urlsplit(page).scheme not in ("http", "https"):
              return ask_user(question)  # no web origin: ask every time
          # An approval covers only this exact input on this page.
          key = (name, page, detail)
          if key not in granted and ask_user(question):
              granted.add(key)
          return key in granted

      return confirm


  # A MyBrowser that also implements javascript_exec and file_upload
  # file_upload also needs the file_policy from "Confine uploads and downloads"
  browser = MyBrowser(
      backend,
      configs={"javascript_exec": {"enabled": True}, "file_upload": {"enabled": True}},
      confirm=make_confirm(),
      url_policy=url_policy,
  )
  ```

  ```typescript TypeScript
  import type { BetaConfirmContext } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const GATED = new Set(["javascript_exec", "file_upload"]);

  /** A value as JSON, with every character outside printable ASCII escaped. */
  const shown = (value: unknown): string =>
    JSON.stringify(value, null, 2).replace(
      /[^\n\x20-\x7e]/g,
      (match) => `\\u${match.charCodeAt(0).toString(16).padStart(4, "0")}`
    );

  const makeConfirm = () => {
    const granted = new Set<string>();
    return async (ctx: BetaConfirmContext): Promise<boolean> => {
      const name = ctx.member;
      if (!GATED.has(name)) return true;
      const detail = shown(ctx.input);
      const page = ctx.tabURL;
      const where = page ? shown(page) : "a tab with no URL";
      const question = `Allow ${name} on ${where}?\n${detail}`;
      const scheme = page === undefined ? undefined : URL.parse(page)?.protocol;
      if (scheme !== "http:" && scheme !== "https:") {
        return askUser(question); // no web origin: ask every time
      }
      // An approval covers only this exact input on this page.
      const key = `${name} ${page} ${detail}`;
      if (!granted.has(key) && (await askUser(question))) {
        granted.add(key);
      }
      return granted.has(key);
    };
  };

  // A MyBrowser that also implements javascript_exec and file_upload
  // file_upload also needs the filePolicy from "Confine uploads and downloads"
  const browser = new MyBrowser(backend, {
    configs: { javascript_exec: { enabled: true }, file_upload: { enabled: true } },
    confirm: makeConfirm(),
    urlPolicy
  });
  ```
</CodeGroup>

Each call to `make_confirm()` (typescript: `makeConfirm()`) returns a callable with no approvals. Call it once for each toolset, and give each user their own toolset.

An approval covers the page as the last state report showed it, and the page can change before the call runs. Purchases, sent messages, and accepted terms happen through ordinary members such as `left_click` and `type`, so `confirm` can't pick them out by name. To have a person approve them, ask about those members too.

Don't enable `javascript_exec` unless [egress rules](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container) limit the browser's outbound connections to the hosts the task needs. A script can send the page's content to any address that the browser can reach.

A `javascript:` URL in a `navigate` call also runs script in the current page, even when `javascript_exec` is off. `confirm` sees that call as a `navigate`, so the example's `confirm` callable would approve it. Your driver must refuse `javascript:` URLs. In the example, the [URL policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy) refuses them before `confirm` runs.

### Isolate the browser host

Run the browser in a dedicated, minimal-privilege container or VM for each session:

* Run as a non-root user, with a read-only root filesystem where the browser allows it.
* Mount nothing from the host beyond the upload and download directories you configured, if any.
* Keep credentials out of the environment, and start from a fresh browser profile.
* Share no filesystem with other tools Claude can call.

<Warning>
  The browser profile must not be signed in to any account whose data or actions you wouldn't hand to Claude. `javascript_exec` runs with the page's own authority: its cookies, its storage, and its signed-in sessions.
</Warning>

Run the code that calls the API outside the browser's container, because that code holds your API key and the conversation. The tool runner and `tool_result` (typescript: `toolResult`) both run the toolset in that code's process, so the browser doesn't share the toolset's filesystem. Treat the browser as remote: [Remote and hosted browsers](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#remote-and-hosted-browsers) applies.

Treat everything a page returns as untrusted, including page text, screenshots, console and network entries, tab titles, and download names.

### Remote and hosted browsers

Some browsers don't share a filesystem with the process that runs the SDK. Examples are a browser in another container, one you reach at a DevTools URL, and one from a hosted browser service. With these, the URL policy, request interception, and `confirm` still run in your process.

With a hosted browser, the provider controls egress and host isolation. Your own egress policy doesn't apply there, so the driver's request hook is your only check on the browser's requests. Find out what the browser's network can reach.

The shipped path checks don't protect a remote browser. `BetaLocalFilePolicy` (typescript: `BetaNodeFilePolicy`) checks paths on the filesystem of the process that runs the SDK, and the browser reads and writes its own filesystem.

The SDK can't detect that a browser is remote. So for a remote browser, keep `file_upload` off unless your driver checks upload paths where the browser runs, with a `BetaFilePolicy` of its own. A `BetaFilePolicy` vets each upload's paths and document IDs, and decides whether Claude sees a download's path.

Have a remote browser refuse downloads, unless its own host has the download setup from [Confine uploads and downloads](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads).

Keep the provider's API key and the session's connection URL, which can contain a key, out of logs, tool results, and error text. If the provider records sessions, the recording is another copy of everything Claude saw and typed, and the provider's retention terms apply to it.

## Computer toolset

`BetaAbstractComputerToolset20260801` is the class for the [computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool). You subclass it and write one method per tool, such as `screenshot` or `left_click`, against your own desktop automation. Your subclass is the driver. The SDK doesn't include a desktop or a ready-made driver. The [minimal VNC example](https://github.com/anthropics/claude-quickstarts/tree/main/computer-toolset) is in the claude-quickstarts repository, in Python and TypeScript. It controls a desktop over VNC, and it isn't production code.

The class takes `configs`, `confirm`, and `tool_configs` (typescript: `toolConfigs`), and you pass them as you do for the browser class. [Customize a driver](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#customize-a-driver), [Handle errors](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#handle-errors), [Start calls while the response streams](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#start-calls-while-the-response-streams), and [Run without the tool runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#run-without-the-tool-runner) apply to it too, with these differences:

* **Browser-only options:** The class has no [URL policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy), no [file policy](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads), and no [state report](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#report-browser-state).
* **`configs`:** Every tool you implement is on by default. The per-tool settings are listed under [Tool parameters](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#tool-parameters).
* **`confirm`:** If your class implements `type`, `key`, or `hold_key`, the constructor raises a configuration error unless you pass a `confirm` callable or turn those tools off with `configs`. A class that overrides `execute` counts as implementing all three.
* **Skipped calls:** After a failed computer call, the tool runner answers the turn's later computer calls with `Not executed: an earlier computer action in this turn failed.` Browser calls get a different text. In a loop you write, answer the skipped computer calls with that exact text ([Batch actions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#batch-actions)).
* **`execute`:** In TypeScript, an `execute` override types `name` as `BetaComputerMemberName` and `input` as `BetaComputerMemberInput`. Both come from `@anthropic-ai/sdk/resources/beta`.
* **Error text:** The SDK doesn't hide local paths in a computer tool's error text or in the text a tool returns. Claude reads both, cut at 4,096 characters. Catch exceptions in your tools, and raise `ToolError` (throw it in TypeScript) with your own text.

### Write a desktop driver

This driver implements five of the 17 tools listed under [Available actions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#available-actions). A tool you don't implement is sent to the API as disabled, as [Quick start](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#quick-start) explains. In the example, `display` stands for your own wrapper around whatever controls the desktop, such as a VNC client or `xdotool`, and `ask_user` (typescript: `askUser`) stands for your own function that asks a person.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic import Anthropic
  from anthropic.tools.computer import (
      BetaAbstractComputerToolset20260801,
      BetaComputerCursorPositionResult,
      BetaScreenshotResult,
      BetaToolsetCallContext,
  )
  from anthropic.types.beta import (
      BetaComputerCursorPositionInput,
      BetaComputerKeyInput,
      BetaComputerLeftClickInput,
      BetaComputerScreenshotInput,
      BetaComputerTypeInput,
  )


  class MyDesktop(BetaAbstractComputerToolset20260801):
      def __init__(self, display, **options):
          super().__init__(**options)
          self.display = display

      def screenshot(
          self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput
      ) -> BetaScreenshotResult:
          # Claude's coordinates are pixel positions in this image.
          data = self.display.png_base64()
          return BetaScreenshotResult(data=data, media_type="image/png")

      def cursor_position(
          self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
      ) -> BetaComputerCursorPositionResult:
          x, y = self.display.cursor()
          return BetaComputerCursorPositionResult(x=x, y=y)

      def left_click(
          self, context: BetaToolsetCallContext, input: BetaComputerLeftClickInput
      ) -> None:
          # input.coordinate is [x, y], or None to click at the cursor. input.text is a
          # modifier to hold, such as "shift". Nothing to return: Claude reads "Clicked."
          self.display.click(input.coordinate, input.text)

      def type(
          self, context: BetaToolsetCallContext, input: BetaComputerTypeInput
      ) -> None:
          self.display.type(input.text)

      def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> None:
          self.display.press(input.text, input.repeat or 1)

      def close(self) -> None:
          super().close()  # first, so no call is still using the desktop when it closes
          self.display.close()


  client = Anthropic()
  with MyDesktop(
      display,
      # required for type and key; see Run the computer toolset safely
      confirm=lambda context: ask_user(f'Allow the "{context.member}" tool?'),
  ) as desktop:
      runner = client.beta.messages.tool_runner(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=[desktop],
          messages=[
              {"role": "user", "content": "Open the calculator and compute 17 * 23."}
          ],
      )
      for message in runner:
          print(message)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import {
    BetaAbstractComputerToolset20260801,
    type BetaComputerCursorPositionResult,
    type BetaComputerToolsetOptions,
    type BetaScreenshotResult,
    type BetaToolsetCallContext
  } from "@anthropic-ai/sdk/helpers/beta/toolsets";
  import type {
    BetaComputerCursorPositionInput,
    BetaComputerKeyInput,
    BetaComputerLeftClickInput,
    BetaComputerScreenshotInput,
    BetaComputerTypeInput
  } from "@anthropic-ai/sdk/resources/beta";

  class MyDesktop extends BetaAbstractComputerToolset20260801 {
    constructor(private display: Display, options: BetaComputerToolsetOptions = {}) {
      super(options);
    }

    protected override async screenshot(
      ctx: BetaToolsetCallContext,
      input: BetaComputerScreenshotInput
    ): Promise<BetaScreenshotResult> {
      // Claude's coordinates are pixel positions in this image.
      return { data: await this.display.pngBase64(), mediaType: "image/png" };
    }

    protected override async cursor_position(
      ctx: BetaToolsetCallContext,
      input: BetaComputerCursorPositionInput
    ): Promise<BetaComputerCursorPositionResult> {
      const { x, y } = await this.display.cursor();
      return { x, y };
    }

    protected override async left_click(
      ctx: BetaToolsetCallContext,
      input: BetaComputerLeftClickInput
    ): Promise<void> {
      // input.coordinate is [x, y], or null or undefined to click at the cursor. input.text
      // is a modifier to hold, such as "shift". Nothing to return: Claude reads "Clicked."
      await this.display.click(input.coordinate, input.text);
    }

    // The type tool is spelled type_ in TypeScript.
    protected override async type_(
      ctx: BetaToolsetCallContext,
      input: BetaComputerTypeInput
    ): Promise<void> {
      await this.display.type(input.text);
    }

    protected override async key(
      ctx: BetaToolsetCallContext,
      input: BetaComputerKeyInput
    ): Promise<void> {
      await this.display.press(input.text, input.repeat ?? 1);
    }

    override async close(): Promise<void> {
      await super.close(); // first, so no call is still using the desktop when it closes
      await this.display.close();
    }
  }

  const client = new Anthropic();
  const desktop = new MyDesktop(display, {
    // required for type and key; see Run the computer toolset safely
    confirm: (ctx) => askUser(`Allow the "${ctx.member}" tool?`)
  });
  try {
    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: [desktop],
      messages: [{ role: "user", content: "Open the calculator and compute 17 * 23." }]
    });
    for await (const message of runner) console.log(message);
  } finally {
    await desktop.close();
  }
  ```
</CodeGroup>

<Warning>
  The `confirm` in this example asks a person before every call the driver runs. Before you run the driver against anything but a throwaway machine, read [Run the computer toolset safely](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#run-the-computer-toolset-safely).
</Warning>

Four tools have no input fields: `screenshot`, `cursor_position`, `left_mouse_down`, and `left_mouse_up`. Every input type, including theirs, comes from `anthropic.types.beta` (typescript: `@anthropic-ai/sdk/resources/beta`).

In TypeScript, write tools as methods, not arrow-function fields. [Implement a driver](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#implement-a-driver) gives the reason.

### Scale coordinates and size images

Every point Claude sends is a pixel position in the screenshots you return: each `coordinate` and `start_coordinate`, and both corners of a `zoom` `region`. The SDK passes them to your tools unchanged.

If your screenshots are a different size from the display, convert in both directions in your driver: Claude's points to display pixels, and the cursor position you report to screenshot pixels. Keep the screenshot size the same for the whole session, and give it the display's aspect ratio:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.tools import ToolError

  SCREENSHOT_SIZE = (1280, 720)  # the size of every full screenshot the driver returns
  DISPLAY_SIZE = (2560, 1440)


  def to_display(coordinate: list[int]) -> tuple[int, int]:
      x, y = coordinate
      width, height = SCREENSHOT_SIZE
      if not (0 <= x < width and 0 <= y < height):
          # Refuse the point. Moving it into range would click where Claude didn't choose.
          raise ToolError(f"[{x}, {y}] is outside the {width}x{height} screenshot")
      return x * DISPLAY_SIZE[0] // width, y * DISPLAY_SIZE[1] // height


  def to_screenshot(x: int, y: int) -> tuple[int, int]:
      width, height = DISPLAY_SIZE
      return x * SCREENSHOT_SIZE[0] // width, y * SCREENSHOT_SIZE[1] // height


  to_display([640, 360])  # (1280, 720)
  ```

  ```typescript TypeScript
  import { ToolError } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const SCREENSHOT_SIZE = { width: 1280, height: 720 }; // the size of every full screenshot
  const DISPLAY_SIZE = { width: 2560, height: 1440 };

  function toDisplay(coordinate: number[]): [number, number] {
    const [x, y] = coordinate;
    const { width, height } = SCREENSHOT_SIZE;
    if (x < 0 || x >= width || y < 0 || y >= height) {
      // Refuse the point. Moving it into range would click where Claude didn't choose.
      throw new ToolError(`[${x}, ${y}] is outside the ${width}x${height} screenshot`);
    }
    return [
      Math.floor((x * DISPLAY_SIZE.width) / width),
      Math.floor((y * DISPLAY_SIZE.height) / height)
    ];
  }

  function toScreenshot(x: number, y: number): [number, number] {
    return [
      Math.floor((x * SCREENSHOT_SIZE.width) / DISPLAY_SIZE.width),
      Math.floor((y * SCREENSHOT_SIZE.height) / DISPLAY_SIZE.height)
    ];
  }

  toDisplay([640, 360]); // [1280, 720]
  ```
</CodeGroup>

Call `to_display` (typescript: `toDisplay`) on each `coordinate` and `start_coordinate` before you act on it, and `to_screenshot` (typescript: `toScreenshot`) on the position that `cursor_position` reports. A click or scroll with no `coordinate` acts at the cursor, so it has nothing to convert. Scale a `zoom` `region` by the same factor. A `zoom` image doesn't change this: the next points Claude sends are still pixel positions in the full screenshot.

The SDK never reads or resizes an image. The API rejects an image over the model's limits, which ends the run. Scale each screenshot and `zoom` image in the driver. See [Size screenshots to fit image limits](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions). On a long run, one request can hold more than 20 images, and the API then holds each one to a stricter limit. See [Manage screenshot history](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#manage-screenshot-history).

### Input checks and results

Don't rely on the SDK to check a call's input. Have your driver check the fields it uses and refuse a call it can't run: raise `ToolError` (throw it in TypeScript). Claude reads the message and can send a corrected call.

Neither SDK limits a `duration`, a `repeat` count, or a `scroll_amount`. Step 4 under [Run the computer toolset safely](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#run-the-computer-toolset-safely) covers them.

What a tool returns determines what Claude reads:

| Tool                 | Returns                            | Claude reads                                                                                |
| -------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------- |
| `screenshot`, `zoom` | `BetaScreenshotResult`             | One image block                                                                             |
| `cursor_position`    | `BetaComputerCursorPositionResult` | `X={x},Y={y}`                                                                               |
| Every other tool     | Nothing, or one line of text       | A short confirmation, such as `Clicked.`, then the returned line in a text block of its own |

### Run the computer toolset safely

What's on the screen steers Claude's next action. A page or a notification can try to make Claude type into the wrong window, or trigger an action with real effects.

<Warning>
  A driver that implements `type`, `key`, or `hold_key` needs a `confirm` callable. Without one, the constructor raises a configuration error, unless `configs` turns those tools off. The SDK itself asks no one: it runs every call that your `confirm` approves, and with no `confirm` it runs every call, including every click. Every computer tool you implement is on by default.
</Warning>

Before you run a driver against anything but a throwaway machine, take these five steps:

1. Isolate the desktop. Run it in a dedicated, minimal-privilege container or VM for each session, with no credentials and no host mounts. Install only the applications the task needs. Run the code that calls the API outside it.
2. Gate actions that have real effects with `confirm`. A purchase or a sent message is an ordinary `left_click`, `type`, or `key`, and `confirm` receives the tool and its input, not the screen. So choose which tools need approval based on the applications Claude can reach on the desktop.
3. Keep terminals, run dialogs, and launchers off the desktop unless the task needs one. When one has keyboard focus, `type`, `key`, and `hold_key` run whatever Claude types, and a click can start a program. If the task needs one, ask a person before keyboard input and clicks, and isolate the desktop so that a command can reach no further than the task needs.
4. Refuse input your desktop shouldn't honor, such as a point outside the screenshot, a `wait` of several minutes, or a very large `repeat` or `scroll_amount`. Raise `ToolError` (throw it in TypeScript) instead of moving the value into range.
5. Treat everything on the screen as untrusted, including window titles and clipboard text. Don't run it or pass it on unchecked.

The SDK applies step 2 through the callable you pass. The other steps are up to your driver and your deployment. The precautions under [Security considerations](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#security-considerations) apply as well.

The following `confirm` asks a person before any keyboard input, through your own `ask_user` (typescript: `askUser`) function, and approves every other call. `context.member` (typescript: `ctx.member`) is the tool's name. To have a person approve clicks too, set `ASK_FIRST` to `KEYBOARD | CLICKS` (typescript: `new Set([...KEYBOARD, ...CLICKS])`).

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.tools.computer import BetaComputerConfirmContext

  KEYBOARD = {"type", "key", "hold_key"}
  CLICKS = {
      "left_click",
      "right_click",
      "middle_click",
      "double_click",
      "triple_click",
      "left_click_drag",
      "left_mouse_down",
      "left_mouse_up",
  }
  ASK_FIRST = KEYBOARD


  def confirm(context: BetaComputerConfirmContext) -> bool:
      if context.member not in ASK_FIRST:
          return True
      # shown is the function from "Gate consequential members".
      detail = shown(context.input.to_dict())
      return ask_user(f'Allow the "{context.member}" tool with this input?\n{detail}')


  desktop = MyDesktop(display, confirm=confirm)
  ```

  ```typescript TypeScript
  import type { BetaComputerConfirmContext } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const KEYBOARD = ["type", "key", "hold_key"];
  const CLICKS = [
    "left_click",
    "right_click",
    "middle_click",
    "double_click",
    "triple_click",
    "left_click_drag",
    "left_mouse_down",
    "left_mouse_up"
  ];
  const ASK_FIRST = new Set(KEYBOARD);

  async function confirm(ctx: BetaComputerConfirmContext): Promise<boolean> {
    if (!ASK_FIRST.has(ctx.member)) return true;
    // shown is the function from "Gate consequential members".
    return askUser(`Allow the "${ctx.member}" tool with this input?\n${shown(ctx.input)}`);
  }

  const desktop = new MyDesktop(display, { confirm });
  ```
</CodeGroup>

A refused call gets an error result, and the run continues. For a refused `type` call, Claude reads `The user did not grant permission to run 'type'. Do not retry it unless the user asks you to.`

This `confirm` approves every tool that isn't in `ASK_FIRST`, including any tool you add later. To fail closed, approve only the tools with no effect on the desktop (`screenshot`, `zoom`, `cursor_position`, and `wait`) and ask about every other tool.

### Use both toolsets in one request

Pass both instances in `tools`. Each call carries its `toolset_name`, `browser` or `computer`, and the tool runner sends the call to the matching instance. After a failed call, the tool runner skips only the turn's later calls to the same toolset, so a failed computer call doesn't skip the turn's browser calls.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  # MyBrowser, backend, and url_policy are from the quick start.
  # confirm is the function from "Run the computer toolset safely".
  with (
      MyBrowser(backend, url_policy=url_policy) as browser,
      MyDesktop(display, confirm=confirm) as desktop,
  ):
      runner = client.beta.messages.tool_runner(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=[browser, desktop],
          messages=[
              {
                  "role": "user",
                  "content": "Copy the heading on example.com into the open text editor.",
              }
          ],
          stream=True,
          run_tools_eagerly=True,  # so a call can start before the response ends
      )
      for stream in runner:
          print(stream.get_final_message())
  ```

  ```typescript TypeScript
  // MyBrowser, backend, and urlPolicy are from the quick start.
  // confirm is the function from "Run the computer toolset safely".
  const browser = new MyBrowser(backend, { urlPolicy });
  const desktop = new MyDesktop(display, { confirm });
  try {
    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: [browser, desktop],
      messages: [
        { role: "user", content: "Copy the heading on example.com into the open text editor." }
      ],
      stream: true,
      runToolsEagerly: true // so a call can start before the response ends
    });
    for await (const stream of runner) console.log(await stream.finalMessage());
  } finally {
    await Promise.all([browser.close(), desktop.close()]);
  }
  ```
</CodeGroup>

In a loop you write, answer each call with `tool_result` (typescript: `toolResult`) on the instance whose `toolset_name` (typescript: `toolsetName`) matches the call's `toolset_name`. In each turn, track failed calls for each toolset separately, and answer a skipped call with that toolset's own text. [Run without the tool runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#run-without-the-tool-runner) has the browser's text, and the Skipped calls bullet at the top of this section has the computer's.

## Reference

The constructor options have the same meaning in both SDKs:

| Python                      | TypeScript     | Sets                                                                 |
| --------------------------- | -------------- | -------------------------------------------------------------------- |
| `configs`                   | `configs`      | Which members are enabled                                            |
| `confirm`                   | `confirm`      | The callable that approves or refuses each call                      |
| `url_policy`                | `urlPolicy`    | Your URL policy, which the SDK calls before each `navigate` to a URL |
| `file_policy`               | `filePolicy`   | Upload roots and download path exposure                              |
| `tool_configs`              | `toolConfigs`  | Fields for the `tools` entry, such as `cache_control`                |
| The `_browser_state` method | `browserState` | The state report                                                     |

The browser class takes every option in the table. The computer class takes `configs`, `confirm`, and `tool_configs` (typescript: `toolConfigs`).

You can't change an option after construction. The [Python browser toolset guide](https://github.com/anthropics/anthropic-sdk-python/blob/main/browser-toolset.md), the [TypeScript browser toolset guide](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/browser-toolset.md), the [Python computer toolset guide](https://github.com/anthropics/anthropic-sdk-python/blob/main/computer-toolset.md), and the [TypeScript computer toolset guide](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/computer-toolset.md) describe each option. The Python guides also cover the async classes, `BetaAsyncAbstractBrowserToolset20260801` and `BetaAsyncAbstractComputerToolset20260801`.

## Limitations

* **The URL policy sees only `navigate` calls:** It doesn't see the requests a page makes, or pages that open any other way, such as from a link Claude clicks or a redirect. See [Intercept requests in the driver](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver).
* **An approval is based on the last state report:** The page can change after that report. The SDK doesn't check the page again before the call runs.
* **Calls on one toolset run one at a time:** You can't turn this off.
* **The SDK doesn't check that tab IDs are unique or how many tabs there are, and doesn't always check that one tab is active:** The API rejects a report that breaks those rules.
* **For a computer call, `confirm` receives the tool and its input, not the screen:** You can't tell from them what a click at a given point does.
* **The SDK doesn't resize a computer toolset's images:** The API rejects an image over the model's limits. See [Scale coordinates and size images](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk#scale-coordinates-and-size-images).

## Next steps

<CardGroup cols={2}>
  <Card title="Browser use tool" icon="browser" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool">
    The member tools, the `browser_state` block, and the tool's security considerations.
  </Card>

  <Card title="Computer use tool" icon="computer" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool">
    The 17 tools, coordinates and image limits, and the tool's security considerations.
  </Card>

  <Card title="Tool runner (SDK)" icon="arrows-clockwise" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner">
    How the SDK runs the loop, and how to change the messages it sends.
  </Card>

  <Card title="Mitigate jailbreaks and prompt injections" icon="shield" href="https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks">
    Guardrails for any application that reads untrusted content.
  </Card>
</CardGroup>

---
title: Tool combinations
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-combinations
description: Common Anthropic tool pairings for research agents, coding agents, and long-running agents.
---

Anthropic-provided tools are designed to work together. Common agent patterns pair tools that cover complementary stages of a workflow: one tool gathers or discovers, another processes or acts. The combinations below are starting points, not prescriptions. Mix them to fit your task.

Each snippet shows only the `tools` array. See [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) for the full request shape.

## Research agent: web\_search + code\_execution

Search finds sources; code execution analyzes and synthesizes. Claude searches for data, then writes Python to process, tabulate, or visualize it. This pairing is a good fit for questions that require both up-to-date information and nontrivial computation over that information, such as "compare this quarter's earnings across the top five cloud providers."

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "code_execution_20260521", "name": "code_execution" }
  ]
}
```

The flow is typically search, then execute, then optionally search again if the first pass surfaced a gap. Code execution runs server-side, so there's no client-side sandbox to manage.

## Coding agent: text\_editor + bash

The text editor reads and modifies files; bash runs tests and build commands. This is the canonical software-development loop: inspect the code, make an edit, run the tests, repeat. Both tools are client-executed, so your application controls which files and commands are accessible.

```json
{
  "tools": [
    { "type": "text_editor_20250728", "name": "str_replace_based_edit_tool" },
    { "type": "bash_20250124", "name": "bash" }
  ]
}
```

Pair this with a constrained working directory and a command allowlist if the agent operates on untrusted code. See [Text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool) and [Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) for the execution contracts.

## Cite-then-fetch: web\_search + web\_fetch

Search surfaces candidate URLs; fetch retrieves full page content for the relevant ones. This avoids fetching everything upfront. Claude runs a search, inspects the snippets, picks the two or three results that actually look relevant, and fetches only those.

```json
{
  "tools": [
    { "type": "web_search_20260209", "name": "web_search" },
    { "type": "web_fetch_20260209", "name": "web_fetch" }
  ]
}
```

This pairing is useful when the answer lives in long-form content (documentation pages, articles, specifications) that a search snippet can't fully capture. Fetch pulls the complete page so Claude can cite specific passages.

## Long-running agent: memory + any other tools

Memory persists state across conversations; the other tools do the work. Add memory to any agent that needs to remember prior sessions, such as a support agent that recalls a customer's earlier issues or a project assistant that tracks decisions made last week.

```json
{
  "tools": [{ "type": "memory_20250818", "name": "memory" }]
}
```

Add your other tools alongside `memory` in the same array.

Memory is orthogonal to your other tools. It doesn't change how they behave; it gives Claude a place to write down and later retrieve facts that would otherwise be lost when the context window resets. See [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) for the storage model.

## All-in-one: computer\_use

The computer use tool subsumes most others by operating a full desktop. Claude sees screenshots and issues mouse and keyboard actions, which means it can drive any application a human can. Use this when the task requires arbitrary GUI interaction that more specific tools can't reach: legacy software without an API, visual verification steps, or workflows that span multiple desktop apps.

```json
{
  "tools": [{ "type": "computer_toolset_20260801" }]
}
```

The toolset entry takes no `name` or display dimensions: coordinates are expressed in the pixel space of the screenshots you return, and you can turn individual actions off through the entry's `configs` field.

Computer use is the most general option and also the slowest, because Claude typically needs a fresh screenshot after each batch of actions. Prefer narrower tools when they cover your use case, and reach for computer use when nothing else fits. If the task stays inside a web browser, use the browser agent pattern in the next section. See [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) for the sandbox setup.

## Browser agent: browser\_use

When the whole task happens inside webpages (filling forms, reading page content, working across tabs), the browser use tool is a closer fit than computer use. Your application drives a browser it controls and returns screenshots or page state; Claude calls page-aware member tools such as `read_page`, `find`, `form_input`, and `get_page_text` alongside clicks and typing, so it can act on element references in addition to pixel coordinates.

```json
{
  "tools": [{ "type": "browser_toolset_20260801" }]
}
```

Like the computer use toolset, the entry takes no `name`, and you turn individual member tools off through its `configs` field. See [Browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) for the execution contract.

## Next steps

<CardGroup cols={2}>
  <Card title="Tool reference" icon="book" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference">
    Full catalog of Anthropic-provided tools with type strings and parameters.
  </Card>

  <Card title="Tool use overview" icon="map" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview">
    How tool use works and when to use Anthropic tools versus defining your own.
  </Card>
</CardGroup>


---
title: Programmatic tool calling
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling
description: Let Claude call your tools from code in the code execution container, cutting model round trips and token use in multi-tool workflows.
featureMetadata:
  status: ga
  zdr: not-eligible
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-opus-5-5
    - claude-opus-5
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-sonnet-4-6
    - claude-sonnet-4-5-20250929
    - claude-haiku-5-5
  supportedPlatforms:
    Claude API: ga
    Claude Platform on AWS: ga
    Amazon Bedrock: not available
    Google Cloud: not available
    Microsoft Foundry:
      availability: ga
      note: On [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry), programmatic tool calling requires a [Hosted on Anthropic deployment](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).
  details:
    - Programmatic tool calling requires the code execution tool with the `code_execution_20260120` or later [tool version](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#tool-versions).
    - Claude Haiku 4.5 accepts the `code_execution_20260120` and later tool versions but doesn't support programmatic tool calling.
---

Programmatic tool calling allows Claude to write code that calls your tools programmatically within a [code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) container, rather than requiring round trips through the model for each tool invocation. This reduces latency for multi-tool workflows and decreases token consumption by allowing Claude to filter or process data before it reaches the model's context window. On agentic search benchmarks like [BrowseComp](https://arxiv.org/abs/2504.12516) and [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), which test multistep web research and complex information retrieval, adding programmatic tool calling on top of basic search tools improved performance by an average of 11% while using 24% fewer input tokens (see [Improved web search with dynamic filtering](https://claude.com/blog/improved-web-search-with-dynamic-filtering)).

Consider checking budget compliance across 20 employees: the traditional approach requires 20 separate model round-trips, pulling thousands of expense line items into the context along the way. With programmatic tool calling, a single script runs all 20 lookups, filters the results, and returns only the employees who exceeded their limits, shrinking what Claude needs to reason over from hundreds of kilobytes down to a handful of lines.

<Tip>
  For a deeper look at the inference and context costs that programmatic tool calling addresses, see [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use).
</Tip>

Programmatic tool calling requires the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) with tool version `code_execution_20260120` or later. To check whether a model supports programmatic tool calling before you send a request, read its `capabilities.code_execution.supported` value from the Models API. [Using the Models API](https://platform.claude.com/docs/en/models/overview#using-the-models-api) describes the field.

## Quick start

Here's an example where Claude programmatically queries a database multiple times and aggregates results. Adding `allowed_callers: ["code_execution_20260120"]` to a tool definition is what makes that tool callable from within code execution (see [The `allowed_callers` field](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling#the-allowed-callers-field)):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-5-5",
          "max_tokens": 4096,
          "messages": [
              {
                  "role": "user",
                  "content": "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
              }
          ],
          "tools": [
              {
                  "type": "code_execution_20260120",
                  "name": "code_execution"
              },
              {
                  "name": "query_database",
                  "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "sql": {
                              "type": "string",
                              "description": "SQL query to execute"
                          }
                      },
                      "required": ["sql"]
                  },
                  "allowed_callers": ["code_execution_20260120"]
              }
          ]
      }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 4096
  messages:
    - role: user
      content: >-
        Query sales data for the West, East, and Central regions, then
        tell me which region had the highest revenue
  tools:
    - type: code_execution_20260120
      name: code_execution
    - name: query_database
      description: >-
        Execute a SQL query against the sales database. Returns a list
        of rows as JSON objects.
      input_schema:
        type: object
        properties:
          sql:
            type: string
            description: SQL query to execute
        required:
          - sql
      allowed_callers:
        - code_execution_20260120
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue",
          }
      ],
      tools=[
          {"type": "code_execution_20260120", "name": "code_execution"},
          {
              "name": "query_database",
              "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "sql": {"type": "string", "description": "SQL query to execute"}
                  },
                  "required": ["sql"],
              },
              "allowed_callers": ["code_execution_20260120"],
          },
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content:
          "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
      }
    ],
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description:
          "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object" as const,
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Messages = [
          new() {
              Role = Role.User,
              Content = "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
          }
      ],
      Tools = [
          new CodeExecutionTool20260120(),
          new ToolUnion(new Tool()
          {
              Name = "query_database",
              Description = "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["sql"] = JsonSerializer.SerializeToElement(new { type = "string", description = "SQL query to execute" }),
                  },
                  Required = ["sql"],
              },
              AllowedCallers = ["code_execution_20260120"]
          }),
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20260120: &anthropic.CodeExecutionTool20260120Param{}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "query_database",
  			Description: anthropic.String("Execute a SQL query against the sales database. Returns a list of rows as JSON objects."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"sql": map[string]any{
  						"type":        "string",
  						"description": "SQL query to execute",
  					},
  				},
  				Required: []string{"sql"},
  			},
  			AllowedCallers: []string{"code_execution_20260120"},
  		}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  import com.anthropic.models.messages.CodeExecutionTool20260120;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .addUserMessage("Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue")
          .addTool(CodeExecutionTool20260120.builder().build())
          .addTool(Tool.builder()
              .name("query_database")
              .description("Execute a SQL query against the sales database. Returns a list of rows as JSON objects.")
              .inputSchema(InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "sql", Map.of(
                          "type", "string",
                          "description", "SQL query to execute"
                      )
                  )))
                  .putAdditionalProperty("required", JsonValue.from(List.of("sql")))
                  .build())
              .allowedCallers(List.of(Tool.AllowedCaller.of("code_execution_20260120")))
              .build())
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue'],
      ],
      model: 'claude-opus-5-5',
      tools: [
          [
              'type' => 'code_execution_20260120',
              'name' => 'code_execution',
          ],
          [
              'name' => 'query_database',
              'description' => 'Execute a SQL query against the sales database. Returns a list of rows as JSON objects.',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'sql' => [
                          'type' => 'string',
                          'description' => 'SQL query to execute',
                      ],
                  ],
                  'required' => ['sql'],
              ],
              'allowed_callers' => ['code_execution_20260120'],
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Query sales data for the West, East, and Central regions, then tell me which region had the highest revenue"
      }
    ],
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description: "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object",
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

The response stops with `stop_reason: "tool_use"`, a `container` ID, and a `tool_use` block for `query_database` whose `caller` field identifies the code execution run that called it. Return the result as shown in [Step 3 of the example workflow](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling#step-3-provide-tool-result) so the code can finish.

## How programmatic tool calling works

When you configure a tool to be callable from code execution and Claude determines that tool is needed:

1. Claude writes Python code that invokes the tool as a function, potentially including multiple tool calls and pre/post-processing logic
2. Claude runs this code in a sandboxed container through code execution
3. When a tool function is called, code execution pauses and the API returns a `tool_use` block
4. You provide the tool result, and code execution continues (intermediate results are not loaded into Claude's context window)
5. Once all code execution completes, Claude receives the final output and continues working on the task

This approach is particularly useful for:

* **Large data processing:** Filter or aggregate tool results before they reach Claude's context
* **Multistep workflows:** Save tokens and latency by calling tools serially or in a loop without sampling Claude in-between tool calls
* **Conditional logic:** Make decisions based on intermediate tool results

<Note>
  Tools that allow a code execution caller are exposed to Claude's code as async Python functions, so Claude can run them in parallel with `asyncio.gather`. Each function takes a single dict of arguments and returns a string: the text of the `tool_result` you send back. Claude's code awaits these functions with top-level `await` and parses results that it needs as structured data, for example `rows = json.loads(await query_database({"sql": "<sql>"}))`.
</Note>

## Core concepts

### The `allowed_callers` field

The `allowed_callers` field specifies which contexts can invoke a tool:

```json
{
  "name": "query_database",
  "description": "Execute a SQL query against the database",
  "input_schema": {
    // ...
  },
  "allowed_callers": ["code_execution_20260120"]
}
```

**Possible values:**

* `["direct"]` - Claude is guided to call this tool directly (default if omitted)
* `["code_execution_20260120"]` - Claude is guided to call this tool only from within code execution
* `["direct", "code_execution_20260120"]` - Claude may call this tool directly or from within code execution

Both `"code_execution_20260120"` and `"code_execution_20260521"` are accepted in `allowed_callers` and are interchangeable: a request using either code-execution tool version satisfies tools that list either caller. Response blocks always tag the caller as `code_execution_20260120` regardless of which version the request declared.

<Tip>
  Choose either `["direct"]` or `["code_execution_20260120"]` for each tool rather than enabling both, as this provides clearer guidance to Claude for how best to use the tool.
</Tip>

<Note>
  `allowed_callers` controls how the tool is presented to Claude and is validated against `tool_choice`, but it is not a hard API-level block on direct invocation. Claude is strongly guided to respect it, but your client should still be prepared to handle a direct `tool_use` for any tool it defines. Do not rely on `allowed_callers` as a security boundary.
</Note>

### The `caller` field in responses

Every tool use block includes a `caller` field indicating how it was invoked:

**Direct invocation (traditional tool use):**

```json
{
  "type": "tool_use",
  "id": "toolu_abc123",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": { "type": "direct" }
}
```

**Programmatic invocation:**

```json
{
  "type": "tool_use",
  "id": "toolu_xyz789",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_abc123"
  }
}
```

The `tool_id` is the `id` of the code execution `server_tool_use` block that made the call, so you can match each programmatic `tool_use` to the code execution run that produced it.

### Container lifecycle

Programmatic tool calling uses the same containers as code execution:

* **Container creation:** A new container is created for each request unless you reuse an existing one
* **Container ID:** Returned in responses in the `container` field, along with an `expires_at` timestamp
* **Reuse:** Pass the container ID back on the next request to keep state. While a programmatic tool call is waiting for your result, the container ID is required on that request, not optional: the API rejects the request without it.
* **Expiration:** `expires_at` tells you how long the container has left. Idle containers are currently reclaimed after about 5 minutes, and no container can be reused more than 30 days after it was created.

<Warning>
  While Claude's code is waiting for a programmatic tool result, the pending call times out after about 4 minutes and raises a `TimeoutError` inside the code. Return each tool result well before the `expires_at` timestamp on the paused response. See [Container expiration during tool call](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling#container-expiration-during-tool-call).
</Warning>

## Example workflow

Here's how a complete programmatic tool calling flow works:

### Step 1: Initial request

Send a request with code execution and a tool that allows programmatic calling. To enable programmatic calling, add the `allowed_callers` field to your tool definition.

<Note>
  Provide detailed descriptions of your tool's output format in the tool description. If you specify that the tool returns JSON, Claude attempts to deserialize and process the result in code. The more detail you provide about the output schema, the better Claude can handle the response programmatically.
</Note>

The request shape is identical to the [Quick start](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling#quick-start) example: include `code_execution` in your tools list, add `allowed_callers: ["code_execution_20260120"]` to any tool you want Claude to invoke from code, and send your user message. The remaining steps in this workflow use the user message `"Query customer purchase history from the last quarter and identify our top 5 customers by revenue"`.

### Step 2: API response with tool call

Claude writes code that calls your tool. The API pauses and returns:

```json Output
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll query the purchase history and analyze the results."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_abc123",
      "name": "code_execution",
      "input": {
        "code": "import json\n\nrows = json.loads(await query_database({'sql': '<sql>'}))\ntop_customers = sorted(rows, key=lambda x: x['revenue'], reverse=True)[:5]\nprint(f'Top 5 customers: {top_customers}')"
      }
    },
    {
      "type": "tool_use",
      "id": "toolu_def456",
      "name": "query_database",
      "input": { "sql": "<sql>" },
      "caller": {
        "type": "code_execution_20260120",
        "tool_id": "srvtoolu_abc123"
      }
    }
  ],
  "container": {
    "id": "container_xyz789",
    "expires_at": "2026-01-20T14:30:00Z"
  },
  "stop_reason": "tool_use"
}
```

### Step 3: Provide tool result

Send the full conversation history plus your tool result. Three details matter on this request:

* The user message that carries your result can contain only `tool_result` blocks. See [Message formatting restrictions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling#message-formatting-restrictions).
* Pass the `container` ID from the paused response. The API rejects a continuation that has pending programmatic tool calls but no container ID.
* Send the same `tools` array as the original request. The code execution tool must still be present for the paused code to resume, and the tools you send on this request are the definitions Claude and the running code can use for the rest of the turn.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-5-5",
          "max_tokens": 4096,
          "container": "container_xyz789",
          "messages": [
              {
                  "role": "user",
                  "content": "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
              },
              {
                  "role": "assistant",
                  "content": [
                      {
                          "type": "text",
                          "text": "I'\''ll query the purchase history and analyze the results."
                      },
                      {
                          "type": "server_tool_use",
                          "id": "srvtoolu_abc123",
                          "name": "code_execution",
                          "input": {"code": "..."}
                      },
                      {
                          "type": "tool_use",
                          "id": "toolu_def456",
                          "name": "query_database",
                          "input": {"sql": "<sql>"},
                          "caller": {
                              "type": "code_execution_20260120",
                              "tool_id": "srvtoolu_abc123"
                          }
                      }
                  ]
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": "toolu_def456",
                          "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}]"
                      }
                  ]
              }
          ],
          "tools": [
              {
                  "type": "code_execution_20260120",
                  "name": "code_execution"
              },
              {
                  "name": "query_database",
                  "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "sql": {
                              "type": "string",
                              "description": "SQL query to execute"
                          }
                      },
                      "required": ["sql"]
                  },
                  "allowed_callers": ["code_execution_20260120"]
              }
          ]
      }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 4096
  container: container_xyz789
  messages:
    - role: user
      content: >-
        Query customer purchase history from the last quarter and identify our
        top 5 customers by revenue
    - role: assistant
      content:
        - type: text
          text: I'll query the purchase history and analyze the results.
        - type: server_tool_use
          id: srvtoolu_abc123
          name: code_execution
          input:
            code: "..."
        - type: tool_use
          id: toolu_def456
          name: query_database
          input:
            sql: "<sql>"
          caller:
            type: code_execution_20260120
            tool_id: srvtoolu_abc123
    - role: user
      content:
        - type: tool_result
          tool_use_id: toolu_def456
          content: >-
            [{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2",
            "revenue": 38000}, ...]
  # Same tools array as the original request
  tools:
    - type: code_execution_20260120
      name: code_execution
    - name: query_database
      description: >-
        Execute a SQL query against the sales database. Returns a list
        of rows as JSON objects.
      input_schema:
        type: object
        properties:
          sql:
            type: string
            description: SQL query to execute
        required:
          - sql
      allowed_callers:
        - code_execution_20260120
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=4096,
      container="container_xyz789",  # Reuse the container
      messages=[
          {
              "role": "user",
              "content": "Query customer purchase history from the last quarter and identify our top 5 customers by revenue",
          },
          {
              "role": "assistant",
              "content": [
                  {
                      "type": "text",
                      "text": "I'll query the purchase history and analyze the results.",
                  },
                  {
                      "type": "server_tool_use",
                      "id": "srvtoolu_abc123",
                      "name": "code_execution",
                      "input": {"code": "..."},
                  },
                  {
                      "type": "tool_use",
                      "id": "toolu_def456",
                      "name": "query_database",
                      "input": {"sql": "<sql>"},
                      "caller": {
                          "type": "code_execution_20260120",
                          "tool_id": "srvtoolu_abc123",
                      },
                  },
              ],
          },
          {
              "role": "user",
              "content": [
                  {
                      "type": "tool_result",
                      "tool_use_id": "toolu_def456",
                      "content": '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]',
                  }
              ],
          },
      ],
      # Same tools array as the original request
      tools=[
          {"type": "code_execution_20260120", "name": "code_execution"},
          {
              "name": "query_database",
              "description": "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "sql": {"type": "string", "description": "SQL query to execute"}
                  },
                  "required": ["sql"],
              },
              "allowed_callers": ["code_execution_20260120"],
          },
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 4096,
    container: "container_xyz789", // Reuse the container
    messages: [
      {
        role: "user",
        content:
          "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
      },
      {
        role: "assistant",
        content: [
          { type: "text", text: "I'll query the purchase history and analyze the results." },
          {
            type: "server_tool_use",
            id: "srvtoolu_abc123",
            name: "code_execution",
            input: { code: "..." }
          },
          {
            type: "tool_use",
            id: "toolu_def456",
            name: "query_database",
            input: { sql: "<sql>" },
            caller: {
              type: "code_execution_20260120",
              tool_id: "srvtoolu_abc123"
            }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: "toolu_def456",
            content:
              '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]'
          }
        ]
      }
    ],
    // Same tools array as the original request
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description:
          "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object" as const,
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      Container = "container_xyz789",
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
          },
          new()
          {
              Role = Role.Assistant,
              Content = new ContentBlock[]
              {
                  new TextBlock { Text = "I'll query the purchase history and analyze the results." },
                  new ServerToolUseBlock
                  {
                      Id = "srvtoolu_abc123",
                      Name = "code_execution",
                      Input = new { code = "..." }
                  },
                  new ToolUseBlock
                  {
                      Id = "toolu_def456",
                      Name = "query_database",
                      Input = new { sql = "<sql>" },
                      Caller = new ToolCaller
                      {
                          Type = "code_execution_20260120",
                          ToolId = "srvtoolu_abc123"
                      }
                  }
              }
          },
          new()
          {
              Role = Role.User,
              Content = new ContentBlockParam[]
              {
                  new ToolResultBlockParam
                  {
                      ToolUseID = "toolu_def456",
                      Content = "[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}, ...]"
                  }
              }
          }
      ],
      // Same tools array as the original request
      Tools = [
          new CodeExecutionTool20260120(),
          new ToolUnion(new Tool()
          {
              Name = "query_database",
              Description = "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["sql"] = JsonSerializer.SerializeToElement(new { type = "string", description = "SQL query to execute" }),
                  },
                  Required = ["sql"],
              },
              AllowedCallers = ["code_execution_20260120"]
          }),
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfString: anthropic.String("container_xyz789"),
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Query customer purchase history from the last quarter and identify our top 5 customers by revenue")),
  		{
  			Role: anthropic.MessageParamRoleAssistant,
  			Content: []anthropic.ContentBlockParamUnion{
  				anthropic.NewTextBlock("I'll query the purchase history and analyze the results."),
  				{OfServerToolUse: &anthropic.ServerToolUseBlockParam{
  					ID:    "srvtoolu_abc123",
  					Name:  anthropic.ServerToolUseBlockParamNameCodeExecution,
  					Input: map[string]any{"code": "..."},
  				}},
  				{OfToolUse: &anthropic.ToolUseBlockParam{
  					ID:    "toolu_def456",
  					Name:  "query_database",
  					Input: map[string]any{"sql": "<sql>"},
  					Caller: anthropic.ServerToolUseBlockParamCallerUnion{
  						OfCodeExecution20260120: &anthropic.ServerToolCaller20260120Param{
  							ToolID: "srvtoolu_abc123",
  						},
  					},
  				}},
  			},
  		},
  		{
  			Role: anthropic.MessageParamRoleUser,
  			Content: []anthropic.ContentBlockParamUnion{
  				{OfToolResult: &anthropic.ToolResultBlockParam{
  					ToolUseID: "toolu_def456",
  					Content: []anthropic.ToolResultBlockParamContentUnion{
  						{OfText: &anthropic.TextBlockParam{
  							Text: `[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]`,
  						}},
  					},
  				}},
  			},
  		},
  	},
  	// Same tools array as the original request
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20260120: &anthropic.CodeExecutionTool20260120Param{}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "query_database",
  			Description: anthropic.String("Execute a SQL query against the sales database. Returns a list of rows as JSON objects."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"sql": map[string]any{
  						"type":        "string",
  						"description": "SQL query to execute",
  					},
  				},
  				Required: []string{"sql"},
  			},
  			AllowedCallers: []string{"code_execution_20260120"},
  		}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  import com.anthropic.models.messages.CodeExecutionTool20260120;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .container("container_xyz789")
          .addUserMessage("Query customer purchase history from the last quarter and identify our top 5 customers by revenue")
          .addAssistantMessageOfBlockParams(List.of(
              ContentBlockParam.ofText(
                  TextBlockParam.builder()
                      .text("I'll query the purchase history and analyze the results.")
                      .build()),
              ContentBlockParam.ofServerToolUse(
                  ServerToolUseBlockParam.builder()
                      .id("srvtoolu_abc123")
                      .name("code_execution")
                      .input(JsonValue.from(Map.of("code", "...")))
                      .build()),
              ContentBlockParam.ofToolUse(
                  ToolUseBlockParam.builder()
                      .id("toolu_def456")
                      .name("query_database")
                      .input(JsonValue.from(Map.of("sql", "<sql>")))
                      .codeExecution20260120Caller("srvtoolu_abc123")
                      .build())
          ))
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofToolResult(
                  ToolResultBlockParam.builder()
                      .toolUseId("toolu_def456")
                      .content("[{\"customer_id\": \"C1\", \"revenue\": 45000}, {\"customer_id\": \"C2\", \"revenue\": 38000}, ...]")
                      .build())
          ))
          // Same tools array as the original request
          .addTool(CodeExecutionTool20260120.builder().build())
          .addTool(Tool.builder()
              .name("query_database")
              .description("Execute a SQL query against the sales database. Returns a list of rows as JSON objects.")
              .inputSchema(InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "sql", Map.of(
                          "type", "string",
                          "description", "SQL query to execute"
                      )
                  )))
                  .putAdditionalProperty("required", JsonValue.from(List.of("sql")))
                  .build())
              .allowedCallers(List.of(Tool.AllowedCaller.of("code_execution_20260120")))
              .build())
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Query customer purchase history from the last quarter and identify our top 5 customers by revenue',
          ],
          [
              'role' => 'assistant',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => "I'll query the purchase history and analyze the results.",
                  ],
                  [
                      'type' => 'server_tool_use',
                      'id' => 'srvtoolu_abc123',
                      'name' => 'code_execution',
                      'input' => ['code' => '...'],
                  ],
                  [
                      'type' => 'tool_use',
                      'id' => 'toolu_def456',
                      'name' => 'query_database',
                      'input' => ['sql' => '<sql>'],
                      'caller' => [
                          'type' => 'code_execution_20260120',
                          'tool_id' => 'srvtoolu_abc123',
                      ],
                  ],
              ],
          ],
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => 'toolu_def456',
                      'content' => '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]',
                  ],
              ],
          ],
      ],
      model: 'claude-opus-5-5',
      container: 'container_xyz789',
      // Same tools array as the original request
      tools: [
          [
              'type' => 'code_execution_20260120',
              'name' => 'code_execution',
          ],
          [
              'name' => 'query_database',
              'description' => 'Execute a SQL query against the sales database. Returns a list of rows as JSON objects.',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'sql' => [
                          'type' => 'string',
                          'description' => 'SQL query to execute',
                      ],
                  ],
                  'required' => ['sql'],
              ],
              'allowed_callers' => ['code_execution_20260120'],
          ],
      ],
  );

  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 4096,
    container: "container_xyz789",
    messages: [
      {
        role: "user",
        content: "Query customer purchase history from the last quarter and identify our top 5 customers by revenue"
      },
      {
        role: "assistant",
        content: [
          {
            type: "text",
            text: "I'll query the purchase history and analyze the results."
          },
          {
            type: "server_tool_use",
            id: "srvtoolu_abc123",
            name: "code_execution",
            input: { code: "..." }
          },
          {
            type: "tool_use",
            id: "toolu_def456",
            name: "query_database",
            input: { sql: "<sql>" },
            caller: {
              type: "code_execution_20260120",
              tool_id: "srvtoolu_abc123"
            }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: "toolu_def456",
            content: '[{"customer_id": "C1", "revenue": 45000}, {"customer_id": "C2", "revenue": 38000}, ...]'
          }
        ]
      }
    ],
    # Same tools array as the original request
    tools: [
      {
        type: "code_execution_20260120",
        name: "code_execution"
      },
      {
        name: "query_database",
        description: "Execute a SQL query against the sales database. Returns a list of rows as JSON objects.",
        input_schema: {
          type: "object",
          properties: {
            sql: {
              type: "string",
              description: "SQL query to execute"
            }
          },
          required: ["sql"]
        },
        allowed_callers: ["code_execution_20260120"]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

### Step 4: Next tool call or completion

The code picks up where it paused and processes your result. Each continuation response either pauses again with more programmatic `tool_use` blocks, or completes the code execution and lets Claude continue the turn (Step 5). Check `stop_reason` and each `tool_use` block's `caller` to tell the two apart: a response that pauses for you has `stop_reason: "tool_use"` and a `tool_use` block whose `caller` names a code execution version, and you repeat Step 3 with a `tool_result` for every pending programmatic call in one user message.

### Step 5: Final response

Once the code execution completes, Claude provides the final response:

```json Output
{
  "content": [
    {
      "type": "code_execution_tool_result",
      "tool_use_id": "srvtoolu_abc123",
      "content": {
        "type": "code_execution_result",
        "stdout": "Top 5 customers: [{'customer_id': 'C1', 'revenue': 45000}, {'customer_id': 'C2', 'revenue': 38000}, {'customer_id': 'C5', 'revenue': 32000}, {'customer_id': 'C8', 'revenue': 28500}, {'customer_id': 'C3', 'revenue': 24000}]",
        "stderr": "",
        "return_code": 0,
        "content": []
      }
    },
    {
      "type": "text",
      "text": "I've analyzed the purchase history from last quarter. Your top 5 customers generated $167,500 in total revenue, with Customer C1 leading at $45,000."
    }
  ],
  "stop_reason": "end_turn"
}
```

## Advanced patterns

### Batch processing with loops

Claude can write code that processes multiple items efficiently:

```python
regions = ["West", "East", "Central", "North", "South"]
results = {}
for region in regions:
    rows = json.loads(await query_database({"sql": f"<sql for {region}>"}))
    results[region] = sum(row["revenue"] for row in rows)

# Process results programmatically
top_region = max(results.items(), key=lambda x: x[1])
print(f"Top region: {top_region[0]} with ${top_region[1]:,} in revenue")
```

This pattern:

* Reduces model round-trips from N (one per region) to 1
* Processes large result sets programmatically before returning to Claude
* Saves tokens by only returning aggregated conclusions instead of raw data

### Early termination

Claude can stop processing as soon as success criteria are met:

```python
endpoints = ["us-east", "eu-west", "apac"]
for endpoint in endpoints:
    status = await check_health({"endpoint": endpoint})
    if status == "healthy":
        print(f"Found healthy endpoint: {endpoint}")
        break  # Stop early, don't check remaining
```

### Conditional tool selection

```python
path = "/tmp/example.txt"
file_info = json.loads(await get_file_info({"path": path}))
if file_info["size"] < 10000:
    content = await read_full_file({"path": path})
else:
    content = await read_file_summary({"path": path})
print(content)
```

### Data filtering

```python
server_id = "srv-01"
log_text = await fetch_logs({"server_id": server_id})
errors = [line for line in log_text.splitlines() if "ERROR" in line]
print(f"Found {len(errors)} errors")
for error in errors[-10:]:  # Only return last 10 errors
    print(error)
```

## Response format

### Programmatic tool call

When code execution calls a tool:

```json
{
  "type": "tool_use",
  "id": "toolu_abc123",
  "name": "query_database",
  "input": { "sql": "<sql>" },
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_xyz789"
  }
}
```

### Tool result handling

Your tool result is passed back to the running code:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_abc123",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000, \"orders\": 23}, {\"customer_id\": \"C2\", \"revenue\": 38000, \"orders\": 18}, ...]"
    }
  ]
}
```

### Code execution completion

When all tool calls are satisfied and code completes:

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_xyz789",
  "content": {
    "type": "code_execution_result",
    "stdout": "Analysis complete. Top 5 customers identified from 847 total records.",
    "stderr": "",
    "return_code": 0,
    "content": []
  }
}
```

## Error handling

### Common errors

| Error                                      | Where it appears                                                             | Description                                                                    | Solution                                                                                                                         |
| ------------------------------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `invalid_tool_input`                       | `error_code` on the `code_execution_tool_result` error block in the response | Invalid parameters were passed to the code execution tool                      | See the [code execution tool errors](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#errors)   |
| `invalid_request_error` (on `tool_choice`) | HTTP 400 error response                                                      | `tool_choice` names a tool whose `allowed_callers` does not include `"direct"` | Either add `"direct"` to that tool's `allowed_callers`, or remove the tool from `tool_choice` and let Claude invoke it from code |

### Container expiration during tool call

If your tool result doesn't arrive within about 4 minutes, the pending call raises a `TimeoutError` inside Claude's running code. Claude sees the error in `stderr` and typically retries the call:

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_abc123",
  "content": {
    "type": "code_execution_result",
    "stdout": "",
    "stderr": "TimeoutError: Calling tool ['query_database'] timed out (no response after 270s).",
    "return_code": 0,
    "content": []
  }
}
```

To prevent timeouts:

* Monitor the `expires_at` field in responses
* Implement timeouts for your tool execution
* Consider breaking long operations into smaller chunks

### Tool execution errors

If your tool returns an error:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_abc123",
  "content": "Error: Query timeout - table lock exceeded 30 seconds"
}
```

Claude's code receives this error and can handle it appropriately.

## Constraints and limitations

### Feature incompatibilities

* **Structured outputs:** Tools with `strict: true` are not supported with programmatic calling
* **Tool choice:** You cannot force programmatic calling of a specific tool through `tool_choice`
* **Parallel tool use:** `disable_parallel_tool_use: true` is not supported with programmatic calling

### Input schema limitations

Custom tools whose `input_schema` contains a recursive `$ref` (a reference cycle, such as a schema that refers to itself) cannot be enabled for programmatic calling. Including a code execution tool version in `allowed_callers` for such a tool causes the request to fail with a `400 invalid_request_error` whose message contains `Circular $ref detected`. The same schema is accepted for direct tool calling.

To work around this, do one of the following:

* Keep the tool direct-only by omitting `allowed_callers` (or setting it to `["direct"]`). Other tools in the same request can still use programmatic calling.
* Remove the cycle from the schema. For example, unroll the recursion to a fixed depth and describe any deeper nesting in the `description` of the innermost level, or replace the recursive property with a plain `{"type": "object"}` whose `description` explains the expected shape.

### Tool restrictions

The following tools cannot be called programmatically:

* Tools provided by an [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
* The [computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) and [browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) toolsets (`computer_toolset_20260801` and `browser_toolset_20260801`), whose `allowed_callers` field accepts only `"direct"`

### Message formatting restrictions

When responding to programmatic tool calls, there are strict formatting requirements:

**Tool result only responses:** If there are pending programmatic tool calls waiting for results, your response message must contain **only** `tool_result` blocks. You cannot include any text content, even after the tool results.

Invalid - Cannot include text when responding to programmatic tool calls:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}]"
    },
    { "type": "text", "text": "What should I do next?" }
  ]
}
```

Valid - Only tool results when responding to programmatic tool calls:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01",
      "content": "[{\"customer_id\": \"C1\", \"revenue\": 45000}]"
    }
  ]
}
```

This restriction only applies when responding to programmatic (code execution) tool calls. For regular client-side tool calls, you can include text content after tool results.

**Text-only tool result content:** The `content` of each `tool_result` that answers a programmatic call must be a string or `text` blocks. Image, document, and other content block types are rejected.

### Rate limits

Programmatic tool calls are subject to the same rate limits as regular tool calls. Each tool call from code execution counts as a separate invocation.

### Validate tool results before use

When implementing user-defined tools that will be called programmatically:

* **Tool results are returned as strings:** They can contain any content, including code snippets or executable commands that may be processed by the execution environment.
* **Validate external tool results:** If your tool returns data from external sources or accepts user input, be aware of code injection risks if the output will be interpreted or executed as code.

## Token efficiency

Programmatic tool calling reduces token consumption in three ways:

* **Tool results from programmatic calls are not added to Claude's context** - only the final code output is
* **Intermediate processing happens in code** - filtering, aggregation, and other transformations don't consume model tokens
* **Multiple tool calls in one code execution** - reduces overhead compared to separate model turns

For example, calling 10 tools directly uses \~10x the tokens of calling them programmatically and returning a summary.

In Anthropic's internal evaluations on a production Claude model:

* On a 75-tool project-management agent benchmark, enabling programmatic tool calling reduced billed input tokens by roughly 38% with no change in task accuracy.
* On [τ²-bench](https://arxiv.org/abs/2506.07982) (airline, retail, and telecom domains), where each turn makes one or two sequential tool calls, programmatic tool calling left scores unchanged and cost roughly 8% more. Sequential single-call workflows do not benefit.
* Across production API traffic, requests whose `tools` array contains 10 to 49 tool definitions see typical token savings of 20% to 40% with programmatic tool calling enabled.

Actual savings vary with workload shape. See [When to use programmatic calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling#when-to-use-programmatic-calling).

## Usage and pricing

Programmatic tool calling uses the same pricing as code execution. See the [code execution pricing](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) for details.

<Note>
  Token counting for programmatic tool calls: Tool results from programmatic invocations do not count toward your input/output token usage. Only the final code execution result and Claude's response count.
</Note>

## Best practices

### Tool design

* **Provide detailed output descriptions:** Because Claude deserializes tool results in code, document the format (JSON structure and field types)
* **Return structured data:** JSON or other machine-readable formats work best for programmatic processing
* **Keep responses concise:** Return only necessary data to minimize processing overhead

### When to use programmatic calling

Programmatic tool calling trades a small fixed overhead (container startup, script generation) for large savings on tool-result tokens and model round-trips. Whether that trade pays off depends on workload shape.

**Strong fit:**

* Fan-out or parallel operations across many items (for example, checking 50 endpoints or looking up 20 records)
* Large tool results that can be filtered, aggregated, or summarized before reaching Claude's context
* Agentic search and retrieval, where iterative querying and result filtering dominate the workflow

**Weak fit:**

* Strictly sequential workflows where each call depends on Claude reasoning over the previous result, because the script cannot skip the model round-trip in that case
* A small number of tool calls with small responses, especially on the first turn of a conversation, where container and script overhead can exceed the savings
* Tools that require immediate user feedback between calls

If you are unsure, measure billed input tokens with and without `allowed_callers` on a representative sample of your traffic before enabling it broadly.

### Performance optimization

* **Reuse containers** when making multiple related requests to maintain state
* **Batch similar operations** in a single code execution when possible

## Troubleshooting

### Common issues

**`invalid_request_error` when setting `tool_choice`**

* `tool_choice` cannot name a tool whose `allowed_callers` omits `"direct"`. Either add `"direct"` to that tool's `allowed_callers`, or remove the tool from `tool_choice` and let Claude invoke it from code.

**Container expiration**

* Respond to each programmatic tool call well before the paused response's `expires_at` timestamp. Claude's code stops waiting for a result after about 4 minutes, and idle containers are currently reclaimed after about 5 minutes.
* Consider implementing faster tool execution

**Tool result not parsed correctly**

* Ensure your tool returns string data that Claude can deserialize
* Provide clear output format documentation in your tool description

### Debugging tips

1. **Log all tool calls and results** to track the flow
2. **Check the `caller` field** to confirm programmatic invocation
3. **Monitor container IDs** to ensure proper reuse
4. **Test tools independently** before enabling programmatic calling

## Why programmatic tool calling works

Claude is trained on large amounts of code, so presenting tools as callable Python functions lets it use that strength:

* **Tool composition:** Chained calls, loops, and conditionals are ordinary Python control flow instead of a series of model round trips
* **Result processing:** Claude's code filters and aggregates large tool outputs, or writes them to files, and only the final output enters the context window
* **Latency:** The model is not re-sampled between the tool calls inside one code execution

## Alternative implementations

Programmatic tool calling is a generalizable pattern that can also be implemented on your own infrastructure. Here's how the approaches compare:

### Client-side direct execution

Provide Claude with a code execution tool and describe what functions are available in that environment. When Claude invokes the tool with code, your application executes it locally where those functions are defined.

**Advantages:**

* Minimal re-architecting of your application
* Full control over the environment and instructions

**Disadvantages:**

* Executes untrusted code outside of a sandbox
* Tool invocations can be vectors for code injection

**Use when:** Your application can safely execute arbitrary code, you want the smallest implementation, and Anthropic's managed offering doesn't fit your needs.

### Self-managed sandboxed execution

Same approach from Claude's perspective, but code runs in a sandboxed container with security restrictions (for example, no network egress). If your tools require external resources, you'll need a protocol for executing tool calls outside the sandbox.

**Advantages:**

* Safe programmatic tool calling on your own infrastructure
* Full control over the execution environment

**Disadvantages:**

* Complex to build and maintain
* Requires managing both infrastructure and inter-process communication

**Use when:** Security is critical and Anthropic's managed solution doesn't fit your requirements.

### Anthropic-managed execution

Anthropic's programmatic tool calling is a managed version of sandboxed execution with an opinionated Python environment tuned for Claude. Anthropic handles container management, code execution, and secure tool invocation communication.

**Advantages:**

* Safe and secure by default
* Enabled with a tool definition, with no infrastructure to run
* Environment and instructions optimized for Claude

Consider using Anthropic's managed solution if you're using the Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws), or [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry). On Microsoft Foundry, programmatic tool calling requires a [Hosted on Anthropic deployment](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).

## Data retention

Programmatic tool calling is built on the code execution infrastructure and uses the same sandbox containers. Container data, including execution artifacts and outputs, is retained for up to 30 days.

For ZDR eligibility across all features, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).

## Next steps

<CardGroup cols={2}>
  <Card title="Fine-grained tool streaming" icon="bolt" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming">
    Stream tool inputs without server-side JSON buffering for latency-sensitive applications.
  </Card>

  <Card title="Code execution tool" icon="code" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool">
    Run Python and bash code in a sandboxed container to analyze data, generate files, and iterate on solutions.
  </Card>

  <Card title="Tool use with Claude" icon="wrench" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview">
    Connect Claude to external tools and APIs. See where tools execute, when Claude calls them, and which tool fits your task.
  </Card>

  <Card title="Define tools" icon="hammer" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools">
    Specify tool schemas, write effective descriptions, and control when Claude calls your tools.
  </Card>
</CardGroup>

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
                  $store[$input['new_path']] = $store[$input['old_path']];
                  unset($store[$input['old_path']]);
                  return "Successfully renamed {$input['old_path']} to {$input['new_path']}";
              default:
                  return "Error: unknown command {$input['command']}";
          }
      },
  );

  $runner = $client->beta->messages->toolRunner(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Remember that customer Acme Corp prefers email follow-ups.']],
      model: Model::CLAUDE_OPUS_5_5,
      tools: [$memory],
      maxIterations: 10,
  );

  $finalMessage = $runner->runUntilDone();
  print_r($finalMessage->content);
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new
  TOOLS = [{type: "memory_20250818", name: "memory"}].freeze

  # An in-memory store that maps memory file paths to their contents.
  # Use your own storage in production.
  STORE = {}

  def execute_memory(input)
    path = input[:path]
    case input[:command]
    when "view"
      if STORE.key?(path)
        lines = STORE[path].chomp.split("\n", -1)
        lines = [""] if lines.empty?
        numbered = lines.each_with_index.map { |line, i| format("%6d\t%s", i + 1, line) }
        "Here's the content of #{path} with line numbers:\n#{numbered.join("\n")}"
      elsif path == "/memories"
        listing = ["1.0K\t/memories"] + STORE.keys.map { |stored| "1.0K\t#{stored}" }
        "Here're the files and directories up to 2 levels deep in #{path}, excluding hidden items and node_modules:\n#{listing.join("\n")}"
      else
        "The path #{path} does not exist. Please provide a valid path."
      end
    when "create"
      STORE[path] = input[:file_text]
      "File created successfully at: #{path}"
    when "str_replace"
      unless STORE.key?(path) && STORE[path].include?(input[:old_str])
        return "No replacement was performed, old_str `#{input[:old_str]}` did not appear verbatim in #{path}."
      end
      STORE[path] = STORE[path].sub(input[:old_str]) { input[:new_str].to_s }
      "The memory file has been edited."
    when "insert"
      return "Error: The path #{path} does not exist" unless STORE.key?(path)
      lines = STORE[path].split("\n", -1)
      lines = [""] if lines.empty?
      if input[:insert_line] < 0 || input[:insert_line] > lines.length
        return "Error: Invalid `insert_line` parameter: #{input[:insert_line]}. It should be within the range of lines of the file: [0, #{lines.length}]"
      end
      lines.insert(input[:insert_line], input[:insert_text].chomp)
      STORE[path] = lines.join("\n")
      "The file #{path} has been edited."
    when "delete"
      return "Error: The path #{path} does not exist" unless STORE.key?(path)
      STORE.delete(path)
      "Successfully deleted #{path}"
    when "rename"
      return "Error: The path #{input[:old_path]} does not exist" unless STORE.key?(input[:old_path])
      return "Error: The destination #{input[:new_path]} already exists" if STORE.key?(input[:new_path])
      STORE[input[:new_path]] = STORE.delete(input[:old_path])
      "Successfully renamed #{input[:old_path]} to #{input[:new_path]}"
    else
      "Error: unknown command #{input[:command]}"
    end
  end

  messages = [{role: "user", content: "Remember that customer Acme Corp prefers email follow-ups."}]
  loop do
    message = client.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 1024,
      messages: messages,
      tools: TOOLS
    )
    unless message.stop_reason == :tool_use
      puts message.content
      break
    end
    tool_results = message.content.filter_map do |block|
      next unless block.type == :tool_use
      {type: "tool_result", tool_use_id: block.id, content: execute_memory(block.input)}
    end
    messages << {role: "assistant", content: message.content} << {role: "user", content: tool_results}
  end
  ```
</CodeGroup>

The in-memory stores in the Go, PHP, and Ruby examples keep them self-contained: each one dispatches on the `command` field in the `tool_use` block's `input` and returns the strings described under [Tool commands](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#tool-commands). A production handler also needs the [path validation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#path-traversal-protection) these demonstration stores skip. For the SDKs' own complete examples, see:

* Python: [examples/memory/basic.py](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/memory/basic.py)
* TypeScript: [examples/tools-helpers-memory.ts](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/examples/tools-helpers-memory.ts)
* C#: [MemoryToolExample](https://github.com/anthropics/anthropic-sdk-csharp/tree/main/examples/MemoryToolExample)
* Java: [BetaMemoryToolExample.java](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/BetaMemoryToolExample.java)

## Tool commands

Your client-side implementation must handle the following commands. These specifications describe the recommended behaviors and return strings: Claude reads whatever text your tool result contains, so you can return different strings if your application needs to.

### view

Shows directory contents or file contents with optional line ranges:

```json
{
  "command": "view",
  "path": "/memories/notes.txt",
  "view_range": [1, 10]
}
```

`view_range` is optional and applies to text-file views: `[start_line, end_line]` returns those lines, and `[start_line, -1]` returns everything from `start_line` to the end of the file.

#### Return values

**For directories:** Return a listing that shows files and directories with their sizes:

```text
Here're the files and directories up to 2 levels deep in {path}, excluding hidden items and node_modules:
{size}\t{path}
{size}\t{path}/{filename1}
{size}\t{path}/{filename2}
```

* Lists files up to 2 levels deep
* Shows human-readable sizes (for example, `5.5K`, `1.2M`)
* Excludes hidden items (files starting with `.`) and `node_modules`
* Uses a tab character between the size and the path

The first `view` of `/memories` on an empty store is not an error. Where your SDK ships a local-filesystem memory tool, `BetaLocalFilesystemMemoryTool`, it creates the memory root before Claude's first call and returns the listing header followed by a single size-and-path line for the empty directory itself.

**For files:** Return file contents with a header and line numbers:

```text wrap
Here's the content of {path} with line numbers:
{line_numbers}{tab}{content}
```

Line number formatting:

* **Width:** 6 characters, right-aligned with space padding
* **Separator:** Tab character between line number and content
* **Indexing:** 1-indexed (first line is line 1)
* **Line limit:** Files with more than 999,999 lines should return an error: `"File {path} exceeds maximum line limit of 999,999 lines."`

**Example output:**

```text
Here's the content of /memories/notes.txt with line numbers:
     1	Hello World
     2	This is line two
    10	Line ten
   100	Line one hundred
```

Claude's tool description also says that `view` displays image files (`.jpg`, `.jpeg`, and `.png`) and truncates the text view of files longer than 16,000 characters. Expect `view` calls on image paths and follow-up ranged views of long files.

#### Error handling

* **File or directory does not exist:** `"The path {path} does not exist. Please provide a valid path."`

### create

Creates a new file:

```json
{
  "command": "create",
  "path": "/memories/notes.txt",
  "file_text": "Meeting notes:\n- Discussed project timeline\n- Next steps defined\n"
}
```

#### Return values

* **Success:** `"File created successfully at: {path}"`

#### Error handling

* **File already exists:** `"Error: File {path} already exists"`

Claude's tool description says `create` "creates or overwrites" a file, so expect `create` calls on paths that already exist. Returning the error is the reference behavior, and overwriting instead is a valid implementation choice.

### str\_replace

Replaces text in a file:

```json
{
  "command": "str_replace",
  "path": "/memories/preferences.txt",
  "old_str": "Favorite color: blue",
  "new_str": "Favorite color: green"
}
```

`new_str` is optional for `str_replace`: when it's omitted, `old_str` is deleted without a replacement.

#### Return values

* **Success:** `"The memory file has been edited."` followed by a snippet of the edited file with line numbers

#### Error handling

* **File does not exist:** `"Error: The path {path} does not exist. Please provide a valid path."`
* **Text not found:** ``"No replacement was performed, old_str `\{old_str}` did not appear verbatim in {path}."``
* **Duplicate text:** When `old_str` appears multiple times, return: ``"No replacement was performed. Multiple occurrences of old_str `\{old_str}` in lines: {line_numbers}. Please ensure it is unique"``

#### Directory handling

If the path is a directory, return a "file does not exist" error.

### insert

Inserts text at a specific line:

```json
{
  "command": "insert",
  "path": "/memories/todo.txt",
  "insert_line": 2,
  "insert_text": "- Review memory tool documentation\n"
}
```

`insert_text` is inserted after line `insert_line`, and `0` inserts at the beginning of the file.

#### Return values

* **Success:** `"The file {path} has been edited."`

#### Error handling

* **File does not exist:** `"Error: The path {path} does not exist"`
* **Invalid line number:** ``"Error: Invalid `insert_line` parameter: {insert_line}. It should be within the range of lines of the file: [0, {n_lines}]"``

#### Directory handling

If the path is a directory, return a "file does not exist" error.

### delete

Deletes a file or directory:

```json
{
  "command": "delete",
  "path": "/memories/old_file.txt"
}
```

#### Return values

* **Success:** `"Successfully deleted {path}"`

#### Error handling

* **File or directory does not exist:** `"Error: The path {path} does not exist"`

#### Directory handling

Deletes the directory and all its contents recursively. The tool description tells Claude it cannot delete the `/memories` directory itself, so reject a `delete` whose path is the memory root.

### rename

Renames or moves a file or directory:

```json
{
  "command": "rename",
  "old_path": "/memories/draft.txt",
  "new_path": "/memories/final.txt"
}
```

#### Return values

* **Success:** `"Successfully renamed {old_path} to {new_path}"`

#### Error handling

* **Source does not exist:** `"Error: The path {old_path} does not exist"`
* **Destination already exists:** Return an error (do not overwrite): `"Error: The destination {new_path} already exists"`

#### Directory handling

Renames the directory. The tool description tells Claude it cannot rename the `/memories` directory itself, so reject a `rename` whose `old_path` is the memory root.

## Prompting guidance

When the memory tool is present in your request's `tools`, the API automatically adds this instruction to the system prompt. You don't need to send it yourself:

```text wrap
IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
MEMORY PROTOCOL:
1. Use the `view` command of your `memory` tool to check for earlier progress.
2. ... (work on the task) ...
   - As you make progress, record status / progress / thoughts etc in your memory.
ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
```

Claude's tool description already tells it to keep the memory directory organized, so you don't need to repeat that instruction. If Claude still creates cluttered memory files, you can reinforce it in your prompt:

```text wrap
Note: when editing your memory folder, always try to keep its content up-to-date, coherent and organized. You can rename or delete files that are no longer relevant. Do not create new files unless necessary.
```

You can also guide what Claude writes to memory. For example: "Only write down information relevant to \<topic> in your memory system."

## Security considerations

Your application executes every file operation Claude requests, so these safeguards are your responsibility:

### Sensitive information

Claude usually refuses to write sensitive information to memory files. For stronger guarantees, add validation that strips sensitive data before your handler writes the file.

### File storage size

Track memory file sizes and cap how large a file can grow. Consider capping how many characters the `view` command returns, and let Claude page through the rest with `view_range`.

### Memory expiration

Periodically delete memory files that haven't been accessed in a long time.

### Path traversal protection

<Warning>
  A malicious path such as `/memories/../../secrets.env` can reach files outside the `/memories` directory. Your implementation must validate every path in every command to prevent directory traversal attacks.
</Warning>

Consider these safeguards:

* Validate that all paths start with `/memories`
* Resolve paths to their canonical form and verify they remain within the memory directory
* Reject paths containing sequences such as `../`, `..\\`, or other traversal patterns
* Watch for URL-encoded traversal sequences (`%2e%2e%2f`)
* Use your language's built-in path security utilities (for example, Python's `pathlib.Path.resolve()` and `relative_to()`)

## Error handling

The memory tool uses similar error-handling patterns to the [text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool#handle-errors). Each command's error messages are listed under [Tool commands](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool#tool-commands). To return an error to Claude, set `is_error` to `true` on the tool result and put the message in `content`:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01C4D5E6F7G8H9I0J1K2L3M4",
  "content": "Error: The path /memories/notes.txt does not exist",
  "is_error": true
}
```

## Context editing integration

The memory tool pairs with context editing to manage long-running conversations. For details, see [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing).

## Using with compaction

The memory tool can also be paired with [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction), which summarizes older conversation context server-side. Context editing clears specific tool results on the client. Compaction automatically summarizes the whole conversation on the server when the conversation approaches the context window limit.

For long-running agents, consider using both: compaction keeps the active context small without client-side bookkeeping, and memory preserves the information that must survive summarization.

## Multisession software development pattern

For software projects that span multiple agent sessions, set up memory files deliberately instead of writing them ad hoc as work progresses. The following pattern turns memory into a recovery mechanism: each new session resumes from the state the last one recorded.

### How the pattern works

1. **Initializer session:** The first session sets up the memory files before any substantive work begins. This includes a progress log (tracking what has been done and what comes next), a feature checklist (defining the scope of work), and a reference to any startup or initialization script the project needs.

2. **Subsequent sessions:** Each new session opens by reading those memory files. This restores the project state without re-exploring the code base or retracing earlier decisions.

3. **End-of-session update:** Before a session ends, it updates the progress log with what was completed and what remains. This ensures the next session has an accurate starting point.

### Key principle

Work on one feature at a time. Mark a feature complete only after end-to-end verification confirms it works, not when the code is written. This keeps the progress log accurate from session to session.

<Tip>
  For a detailed case study of this pattern in practice, including the initializer script, progress file structure, and git-based recovery, see [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
</Tip>

## Next steps

<CardGroup cols={2}>
  <Card title="Bash tool" icon="terminal" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool">
    Execute shell commands in a persistent bash session.
  </Card>

  <Card title="Context editing" icon="edit" href="https://platform.claude.com/docs/en/build-with-claude/context-editing">
    Automatically manage conversation context as it grows with context editing.
  </Card>

  <Card title="Compaction" icon="stack" href="https://platform.claude.com/docs/en/build-with-claude/compaction">
    Server-side context compaction for managing long conversations that approach context window limits.
  </Card>

  <Card title="Tool reference" icon="book" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference">
    Directory of Anthropic-provided tools and reference for optional tool definition properties.
  </Card>
</CardGroup>

---
title: Server tools
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
description: "Work with Anthropic-executed tools: server_tool_use blocks, pause_turn continuation, mixed server and client tool turns, and domain filtering."
---

Server-executed tools share these mechanics: the `server_tool_use` block, `pause_turn` continuation, turns that mix server and client tools, Zero Data Retention (ZDR) eligibility, and domain filtering. For individual tools, see the [tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference).

## The server\_tool\_use block

The `server_tool_use` block appears in Claude's response when a server-executed tool runs. Its `id` field uses the `srvtoolu_` prefix to distinguish it from client tool calls:

```json
{
  "type": "server_tool_use",
  "id": "srvtoolu_01A2B3C4D5E6F7G8H9",
  "name": "web_search",
  "input": { "query": "latest quantum computing breakthroughs" }
}
```

The API executes the tool internally. You see the call and its result in the response, but you don't handle execution. Unlike client `tool_use` blocks, you don't need to respond with a `tool_result`. The tool's result block (for example, `web_search_tool_result` for web search) follows the `server_tool_use` block in the same assistant turn, paired by `tool_use_id`. If Claude calls one of your client tools at the same time, the `server_tool_use` block appears without its result, and the response ends with `stop_reason: "tool_use"`. The API runs the tool when you return the client `tool_result` blocks in your next request.

## The server-side loop and pause\_turn

When using server tools such as web search, the API executes tool calls in a server-side agentic loop. On a long-running turn, the API might pause that loop and return a `pause_turn` stop reason.

Here's how to handle the `pause_turn` stop reason:

<CodeGroup>
  ```bash cURL
  # Initial request. If "stop_reason" in the response is "pause_turn", continue
  # the turn by re-sending the request with the assistant content appended to messages.
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": "Search for comprehensive information about quantum computing breakthroughs in 2025"
        }
      ],
      "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]
    }'
  ```

  ```bash CLI
  # Initial request. If "stop_reason" in the output is "pause_turn", re-run with
  # the assistant content appended to messages (see the SDK tabs).
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tools:
    - {type: web_search_20250305, name: web_search, max_uses: 10}
  messages:
    - {role: user, content: "Search for comprehensive information about quantum computing breakthroughs in 2025"}
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Initial request with web search
  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
          }
      ],
      tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
  )

  # Check if the response has pause_turn stop reason
  if response.stop_reason == "pause_turn":
      # Continue the conversation with the paused content
      messages = [
          {
              "role": "user",
              "content": "Search for comprehensive information about quantum computing breakthroughs in 2025",
          },
          {"role": "assistant", "content": response.content},
      ]

      # Send the continuation request
      continuation = client.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          messages=messages,
          tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}],
      )

      print(continuation)
  else:
      print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Initial request with web search
  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 10
      }
    ]
  });

  // Check if the response has pause_turn stop reason
  if (response.stop_reason === "pause_turn") {
    // Continue the conversation with the paused content
    const messages: Anthropic.MessageParam[] = [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      },
      { role: "assistant", content: response.content }
    ];

    // Send the continuation request
    const continuation = await client.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages,
      tools: [
        {
          type: "web_search_20250305",
          name: "web_search",
          max_uses: 10
        }
      ]
    });

    console.log(continuation);
  } else {
    console.log(response);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [
          new() {
              Role = Role.User,
              Content = "Search for comprehensive information about quantum computing breakthroughs in 2025"
          }
      ],
      Tools = [new ToolUnion(new WebSearchTool20250305 { MaxUses = 10 })]
  };

  var response = await client.Messages.Create(parameters);

  if (response.StopReason?.Value() == StopReason.PauseTurn)
  {
      // Continue the conversation with the paused content
      var continuationParams = new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [
              new() {
                  Role = Role.User,
                  Content = "Search for comprehensive information about quantum computing breakthroughs in 2025"
              },
              new() {
                  Role = Role.Assistant,
                  Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              }
          ],
          Tools = [new ToolUnion(new WebSearchTool20250305 { MaxUses = 10 })]
      };

      var continuation = await client.Messages.Create(continuationParams);
      Console.WriteLine(continuation);
  }
  else
  {
      Console.WriteLine(response);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  webSearchTool := []anthropic.ToolUnionParam{
  	{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{
  		MaxUses: anthropic.Int(10),
  	}},
  }

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Search for comprehensive information about quantum computing breakthroughs in 2025")),
  	},
  	Tools: webSearchTool,
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == anthropic.StopReasonPauseTurn {
  	// Pass the paused response back as-is so Claude can continue the turn
  	continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Search for comprehensive information about quantum computing breakthroughs in 2025")),
  			response.ToParam(),
  		},
  		Tools: webSearchTool,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(continuation)
  } else {
  	fmt.Println(response)
  }
  ```

  ```java Java
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.WebSearchTool20250305;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addUserMessage("Search for comprehensive information about quantum computing breakthroughs in 2025")
          .addTool(WebSearchTool20250305.builder()
              .maxUses(10L)
              .build())
          .build();

      Message response = client.messages().create(params);

      if (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.PAUSE_TURN)) {
          MessageCreateParams continuationParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .addUserMessage("Search for comprehensive information about quantum computing breakthroughs in 2025")
              .addMessage(response)
              .addTool(WebSearchTool20250305.builder()
                  .maxUses(10L)
                  .build())
              .build();

          Message continuation = client.messages().create(continuationParams);
          IO.println(continuation);
      } else {
          IO.println(response);
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => 'Search for comprehensive information about quantum computing breakthroughs in 2025'
          ]
      ],
      model: 'claude-opus-5-5',
      tools: [
          [
              'type' => 'web_search_20250305',
              'name' => 'web_search',
              'max_uses' => 10
          ]
      ],
  );

  if ($response->stopReason === 'pause_turn') {
      $messages = [
          [
              'role' => 'user',
              'content' => 'Search for comprehensive information about quantum computing breakthroughs in 2025'
          ],
          [
              'role' => 'assistant',
              'content' => $response->content
          ]
      ];

      $continuation = $client->messages->create(
          maxTokens: 1024,
          messages: $messages,
          model: 'claude-opus-5-5',
          tools: [
              [
                  'type' => 'web_search_20250305',
                  'name' => 'web_search',
                  'max_uses' => 10
              ]
          ],
      );

      echo $continuation;
  } else {
      echo $response;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Search for comprehensive information about quantum computing breakthroughs in 2025"
      }
    ],
    tools: [
      {
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 10
      }
    ]
  )

  if response.stop_reason == :pause_turn
    messages = [
      {
        role: "user",
        content: "Search for comprehensive information about quantum computing breakthroughs in 2025"
      },
      {
        role: "assistant",
        content: response.content
      }
    ]

    continuation = client.messages.create(
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: messages,
      tools: [
        {
          type: "web_search_20250305",
          name: "web_search",
          max_uses: 10
        }
      ]
    )

    puts continuation
  else
    puts response
  end
  ```
</CodeGroup>

When handling `pause_turn`:

* **Continue the conversation:** Pass the paused response back as-is in a subsequent request to let Claude continue its turn.
* **Preserve tool state:** Include the same tools in the continuation request. A paused turn can end with a `server_tool_use` block whose tool has not run yet, and the API returns a validation error if that tool is missing from the continuation.
* **Repeat as needed:** A continued turn can pause again. Check `stop_reason` on each response and continue until you get a different stop reason, capping the number of continuations as you would any retry loop.

For the other `stop_reason` values and general handling patterns, see [Stop reasons and fallback](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons).

## Mixing server tools and client tools in one turn

Claude can call a server tool and a client tool in the same group of parallel tool calls, for example, `web_fetch` together with a user-defined tool. A client tool is any tool that your code executes and that produces a `tool_use` block, whether it is user-defined or an Anthropic-schema client tool such as the [Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool). When that happens, the API does not run the server tool. It returns immediately so that you can run the client tool first:

* `stop_reason` is `"tool_use"`, not `"pause_turn"`.
* `content` contains the `server_tool_use` block and the client `tool_use` block, but no result block for the server tool: that call is not finished.
* There is no other marker. Detect the state by looking for a `server_tool_use` block whose `id` has no matching result block in the response. An `mcp_tool_use` block from the [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector) behaves the same way. Server tool calls that already have their result block in the same response are complete and need nothing from you.

<Note>
  With [programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling), the same response shape means something different. The client `tool_use` block comes from code that is running in the `code_execution` tool rather than from Claude directly, and its `caller` field names the `code_execution` block that called it. That code has already started: it is paused waiting for your `tool_result` blocks, and sending them resumes the execution instead of starting a deferred tool. The `code_execution` block's own result block arrives once the code finishes, which can take more than one round of tool results. The follow-up user message itself is the same in both cases; with programmatic tool calling, also pass back the `id` from the response's `container` field, as that page shows.
</Note>

```json
{
  "stop_reason": "tool_use",
  "content": [
    {
      "type": "text",
      "text": "I'll fetch the article and check your system at the same time."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01HxbWnMRmbWyMfUtJKC45rA",
      "name": "web_fetch",
      "input": { "url": "https://example.com/article" }
    },
    {
      "type": "tool_use",
      "id": "toolu_01PjgRJLbXrXEMZwDNYLnBqk",
      "name": "run_command",
      "input": { "command": "uname -a" }
    }
  ]
}
```

To continue the turn, run the client tools and send a user message whose content is only the `tool_result` blocks, one for each `tool_use` block in that response. Keep the same `tools` array: a resume request that no longer defines the waiting server tool fails with a 400 whose message ends ``but no `web_fetch` tool was provided``.

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01PjgRJLbXrXEMZwDNYLnBqk",
      "content": "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
    }
  ]
}
```

The API attaches your results to the still-open assistant turn, runs the deferred server tool (for paused code execution, resumes it), and then lets Claude continue. For a server tool Claude called directly, the next response begins with the result block that answers the previous response's `server_tool_use` `id`, followed by the newly generated content and a fresh `stop_reason`:

```json
{
  "stop_reason": "end_turn",
  "content": [
    {
      "type": "web_fetch_tool_result",
      "tool_use_id": "srvtoolu_01HxbWnMRmbWyMfUtJKC45rA",
      "content": {
        "type": "web_fetch_result",
        "url": "https://example.com/article",
        "content": {
          "type": "document",
          "source": {
            "type": "text",
            "media_type": "text/plain",
            "data": "Full text content of the article..."
          }
        }
      }
    },
    {
      "type": "text",
      "text": "The article argues that... and your machine is running Linux..."
    }
  ]
}
```

A `server_tool_use` block and its result block pair up by `tool_use_id`, not by position: in this flow they arrive in two different responses, and the `server_tool_use` block is not repeated in the second one. On later requests, keep the whole exchange in your `messages` array in order: the first response as an `assistant` message, the `tool_result` user message, and then the next response as another `assistant` message, the same way you accumulate any other tool-use exchange.

<Warning>
  The follow-up user message must contain nothing except `tool_result` blocks. A block added after the results, such as text, tells the API that the assistant turn is over. For a server tool Claude called directly, that leaves the turn with an unresolved server tool call, and the request fails with a 400 `invalid_request_error`:

  ```text wrap
  `web_fetch` tool use with id `srvtoolu_01HxbWnMRmbWyMfUtJKC45rA` was found without a corresponding `web_fetch_tool_result` block
  ```

  A follow-up that puts content before the results, answers only some of the client `tool_use` IDs, or contains no `tool_result` blocks at all fails earlier, with the client tool error described in [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls):

  ```text wrap
  `tool_use` ids were found without `tool_result` blocks immediately after: toolu_01PjgRJLbXrXEMZwDNYLnBqk. Each `tool_use` block must have a corresponding `tool_result` block in the next message.
  ```

  To give Claude more input, send it as a separate user message after the turn completes.
</Warning>

**How this differs from `pause_turn`:** A [`pause_turn` response](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn) can also end with a `server_tool_use` block that has not run, but it never leaves a client `tool_use` block waiting on you, so you continue it by re-sending the assistant content as-is. A response that leaves a client `tool_use` block waiting on you never has a `stop_reason` of `pause_turn`: when Claude stops to call your tools, `stop_reason` is `tool_use`, and you continue it by sending the client `tool_result` blocks rather than by re-sending the response. In both cases the API runs the pending server tool at the start of the next request.

The following example enables web fetch together with a user-defined `run_command` tool and handles the mixed response:

<CodeGroup>
  ```bash cURL
  # If "stop_reason" is "tool_use" and a server_tool_use block has no matching
  # result block, that call is not finished. Run the client tools, then POST
  # again with one more user message containing only their tool_result blocks
  # and the same tools array (see the SDK tabs).
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": "Summarize https://example.com/article and run uname -a to tell me what system this is on."
        }
      ],
      "tools": [
        {"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5},
        {
          "name": "run_command",
          "description": "Run a shell command on this computer and return its output.",
          "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "The command to run"}},
            "required": ["command"]
          }
        }
      ]
    }'
  ```

  ```bash CLI
  # If "stop_reason" is "tool_use" and a server_tool_use block has no matching
  # result block, run the client tools and re-run with a user message of only
  # their tool_result blocks appended (see the SDK tabs).
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: "Summarize https://example.com/article and run uname -a to tell me what system this is on."
  tools:
    - {type: web_fetch_20250910, name: web_fetch, max_uses: 5}
    - name: run_command
      description: Run a shell command on this computer and return its output.
      input_schema:
        type: object
        properties:
          command: {type: string, description: The command to run}
        required: [command]
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  tools = [
      {"type": "web_fetch_20250910", "name": "web_fetch", "max_uses": 5},
      {
          "name": "run_command",
          "description": "Run a shell command on this computer and return its output.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "command": {"type": "string", "description": "The command to run"}
              },
              "required": ["command"],
          },
      },
  ]
  messages = [
      {
          "role": "user",
          "content": "Summarize https://example.com/article and run uname -a to tell me what system this is on.",
      }
  ]

  response = client.messages.create(
      model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages
  )

  tool_results = [
      {
          "type": "tool_result",
          "tool_use_id": block.id,
          # Run your tool here. This example returns a fixed string.
          "content": "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux",
      }
      for block in response.content
      if block.type == "tool_use"
  ]

  if response.stop_reason == "tool_use" and tool_results:
      # A server_tool_use block with no result block in this response is not finished; its result arrives in a later response.
      # Send back only the client tool_result blocks, with the same tools.
      continuation = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          tools=tools,
          messages=[
              *messages,
              {"role": "assistant", "content": response.content},
              {"role": "user", "content": tool_results},
          ],
      )
      # If a web_fetch was deferred, it runs on this request and its
      # web_fetch_tool_result is the first block of continuation.content.
      print(continuation)
  else:
      print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const webFetchTool = {
    type: "web_fetch_20250910",
    name: "web_fetch",
    max_uses: 5
  } as const;
  const runCommandTool: Anthropic.Tool = {
    name: "run_command",
    description: "Run a shell command on this computer and return its output.",
    input_schema: {
      type: "object" as const,
      properties: {
        command: { type: "string", description: "The command to run" }
      },
      required: ["command"]
    }
  };
  const messages: Anthropic.MessageParam[] = [
    {
      role: "user",
      content:
        "Summarize https://example.com/article and run uname -a to tell me what system this is on."
    }
  ];

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [webFetchTool, runCommandTool],
    messages
  });

  const toolResults: Anthropic.ToolResultBlockParam[] = [];
  for (const block of response.content) {
    if (block.type === "tool_use") {
      toolResults.push({
        type: "tool_result",
        tool_use_id: block.id,
        // Run your tool here. This example returns a fixed string.
        content: "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
      });
    }
  }

  if (response.stop_reason === "tool_use" && toolResults.length > 0) {
    // A server_tool_use block with no result block in this response is not finished; its result arrives in a later response.
    // Send back only the client tool_result blocks, with the same tools.
    const continuation = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: [webFetchTool, runCommandTool],
      messages: [
        ...messages,
        { role: "assistant", content: response.content },
        { role: "user", content: toolResults }
      ]
    });
    // If a web_fetch was deferred, it runs on this request and its
    // web_fetch_tool_result is the first block of continuation.content.
    console.log(continuation);
  } else {
    console.log(response);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new WebFetchTool20250910() { MaxUses = 5 }),
      new ToolUnion(new Tool()
      {
          Name = "run_command",
          Description = "Run a shell command on this computer and return its output.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["command"] = JsonSerializer.SerializeToElement(
                      new { type = "string", description = "The command to run" }
                  ),
              },
              Required = ["command"],
          },
      }),
  ];
  MessageParam userMessage = new()
  {
      Role = Role.User,
      Content = "Summarize https://example.com/article and run uname -a to tell me what system this is on."
  };

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = tools,
      Messages = [userMessage]
  });

  var toolResults = new List<ContentBlockParam>();
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          toolResults.Add(new ContentBlockParam(new ToolResultBlockParam()
          {
              ToolUseID = toolUse.ID,
              // Run your tool here. This example returns a fixed string.
              Content = "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux",
          }));
      }
  }

  if (response.StopReason?.Value() == StopReason.ToolUse && toolResults.Count > 0)
  {
      // A server_tool_use block with no result block in this response is not finished; its result arrives in a later response.
      // Send back only the client tool_result blocks, with the same tools.
      var continuation = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Tools = tools,
          Messages =
          [
              userMessage,
              new()
              {
                  Role = Role.Assistant,
                  Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new() { Role = Role.User, Content = new MessageParamContent(toolResults) }
          ]
      });
      // If a web_fetch was deferred, it runs on this request and its
      // web_fetch_tool_result is the first block of continuation.Content.
      Console.WriteLine(continuation);
  }
  else
  {
      Console.WriteLine(response);
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  tools := []anthropic.ToolUnionParam{
  	{OfWebFetchTool20250910: &anthropic.WebFetchTool20250910Param{
  		MaxUses: anthropic.Int(5),
  	}},
  	{OfTool: &anthropic.ToolParam{
  		Name:        "run_command",
  		Description: anthropic.String("Run a shell command on this computer and return its output."),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"command": map[string]any{
  					"type":        "string",
  					"description": "The command to run",
  				},
  			},
  			Required: []string{"command"},
  		},
  	}},
  }
  userMessage := anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize https://example.com/article and run uname -a to tell me what system this is on."))

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools:     tools,
  	Messages:  []anthropic.MessageParam{userMessage},
  })
  if err != nil {
  	log.Fatal(err)
  }

  var toolResults []anthropic.ContentBlockParamUnion
  for _, block := range response.Content {
  	if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
  		// Run your tool here. This example returns a fixed string.
  		output := "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
  		toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, output, false))
  	}
  }

  if response.StopReason == anthropic.StopReasonToolUse && len(toolResults) > 0 {
  	// A server_tool_use block with no result block in this response is not finished; its result arrives in a later response.
  	// Send back only the client tool_result blocks, with the same tools.
  	continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Tools:     tools,
  		Messages: []anthropic.MessageParam{
  			userMessage,
  			response.ToParam(),
  			anthropic.NewUserMessage(toolResults...),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	// If a web_fetch was deferred, it runs on this request and its
  	// web_fetch_tool_result is the first block of continuation.Content.
  	fmt.Println(continuation)
  } else {
  	fmt.Println(response)
  }
  ```

  ```java Java
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool runCommandTool = Tool.builder()
          .name("run_command")
          .description("Run a shell command on this computer and return its output.")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "command", Map.of("type", "string", "description", "The command to run")
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("command")))
              .build())
          .build();
      String prompt = "Summarize https://example.com/article and run uname -a to tell me what system this is on.";

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addTool(WebFetchTool20250910.builder().maxUses(5L).build())
          .addTool(runCommandTool)
          .addUserMessage(prompt)
          .build());

      List<ContentBlockParam> toolResults = new ArrayList<>();
      for (ContentBlock block : response.content()) {
          block.toolUse().ifPresent(toolUse -> toolResults.add(ContentBlockParam.ofToolResult(
              ToolResultBlockParam.builder()
                  .toolUseId(toolUse.id())
                  // Run your tool here. This example returns a fixed string.
                  .content("Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux")
                  .build()
          )));
      }

      boolean isToolUse = response.stopReason()
          .map(StopReason.TOOL_USE::equals)
          .orElse(false);
      if (isToolUse && !toolResults.isEmpty()) {
          // A server_tool_use block with no result block in this response is not finished; its result arrives in a later response.
          // Send back only the client tool_result blocks, with the same tools.
          Message continuation = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(WebFetchTool20250910.builder().maxUses(5L).build())
              .addTool(runCommandTool)
              .addUserMessage(prompt)
              .addMessage(response)
              .addUserMessageOfBlockParams(toolResults)
              .build());
          // If a web_fetch was deferred, it runs on this request and its
          // web_fetch_tool_result is the first block of continuation.content().
          IO.println(continuation);
      } else {
          IO.println(response);
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $tools = [
      ['type' => 'web_fetch_20250910', 'name' => 'web_fetch', 'max_uses' => 5],
      [
          'name' => 'run_command',
          'description' => 'Run a shell command on this computer and return its output.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'command' => ['type' => 'string', 'description' => 'The command to run']
              ],
              'required' => ['command']
          ]
      ]
  ];
  $userMessage = ['role' => 'user', 'content' => 'Summarize https://example.com/article and run uname -a to tell me what system this is on.'];

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [$userMessage],
      model: 'claude-opus-4-8',
      tools: $tools,
  );

  $toolResults = [];
  foreach ($response->content as $block) {
      if ($block->type === 'tool_use') {
          $toolResults[] = [
              'type' => 'tool_result',
              'tool_use_id' => $block->id,
              // Run your tool here. This example returns a fixed string.
              'content' => 'Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux'
          ];
      }
  }

  if ($response->stopReason === 'tool_use' && count($toolResults) > 0) {
      // A server_tool_use block with no result block in this response is not finished; its result arrives in a later response.
      // Send back only the client tool_result blocks, with the same tools.
      $continuation = $client->messages->create(
          maxTokens: 1024,
          messages: [
              $userMessage,
              ['role' => 'assistant', 'content' => $response->content],
              ['role' => 'user', 'content' => $toolResults],
          ],
          model: 'claude-opus-4-8',
          tools: $tools,
      );
      // If a web_fetch was deferred, it runs on this request and its
      // web_fetch_tool_result is the first block of $continuation->content.
      echo $continuation;
  } else {
      echo $response;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  tools = [
    { type: "web_fetch_20250910", name: "web_fetch", max_uses: 5 },
    {
      name: "run_command",
      description: "Run a shell command on this computer and return its output.",
      input_schema: {
        type: "object",
        properties: {
          command: { type: "string", description: "The command to run" }
        },
        required: ["command"]
      }
    }
  ]
  user_message = {
    role: "user",
    content: "Summarize https://example.com/article and run uname -a to tell me what system this is on."
  }

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: tools,
    messages: [user_message]
  )

  tool_results = []
  response.content.each do |block|
    next unless block.type == :tool_use

    tool_results << {
      type: "tool_result",
      tool_use_id: block.id,
      # Run your tool here. This example returns a fixed string.
      content: "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
    }
  end

  if response.stop_reason == :tool_use && !tool_results.empty?
    # A server_tool_use block with no result block in this response is not finished; its result arrives in a later response.
    # Send back only the client tool_result blocks, with the same tools.
    continuation = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      tools: tools,
      messages: [
        user_message,
        { role: "assistant", content: response.content },
        { role: "user", content: tool_results }
      ]
    )
    # If a web_fetch was deferred, it runs on this request and its
    # web_fetch_tool_result is the first block of continuation.content.
    puts continuation
  else
    puts response
  end
  ```
</CodeGroup>

This code is also correct when Claude does not mix the two kinds of call. A turn with only client `tool_use` blocks takes the same continuation path, and a turn with only server tool calls needs no client `tool_result` blocks from you: its result blocks are normally already present, and one that comes back suspended, such as a [`pause_turn` response](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn), is re-sent as-is instead.

## ZDR and allowed\_callers

The basic versions of web search (`web_search_20250305`) and web fetch (`web_fetch_20250910`) are eligible for [Zero Data Retention (ZDR)](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).

The `_20260209` and later versions with dynamic filtering are **not** ZDR-eligible by default because dynamic filtering relies on code execution internally.

To use a `_20260209` or later server tool with ZDR, disable dynamic filtering by setting `"allowed_callers": ["direct"]` on the tool:

```json
{
  "type": "web_search_20260209",
  "name": "web_search",
  "allowed_callers": ["direct"]
}
```

This restricts the tool to direct invocation only, bypassing the internal code execution step.

`allowed_callers` controls how a tool can be invoked: directly by Claude (`"direct"`), from inside a code execution container (for example, `"code_execution_20260120"`), or both. The `_20260209` versions of the web tools default to the code execution caller only; earlier versions default to `["direct"]`. On models that don't support programmatic tool calling, these versions require `allowed_callers: ["direct"]`; without it the API returns a validation error that says to set it.

<Note>
  Even when web fetch is used in a ZDR-eligible configuration, website publishers might retain any parameters passed to the URL if Claude fetches content from their site.
</Note>

## Domain filtering

Server tools that access the web accept `allowed_domains` and `blocked_domains` parameters to control which domains Claude can reach. Both are fields on the tool object:

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "allowed_domains": ["example.com", "docs.python.org"]
}
```

When using domain filters:

* Domains should not include the HTTP/HTTPS scheme (use `example.com` instead of `https://example.com`).
* Subdomains are automatically included (`example.com` covers `docs.example.com`).
* Specific subdomains restrict results to only that subdomain (`docs.example.com` returns only results from that subdomain, not from `example.com` or `api.example.com`).
* Subpaths are supported for web search and match anything after the path (`example.com/blog` matches `example.com/blog/post-1`).
* Web fetch matches on the domain only: an entry that includes a path never matches a web fetch URL.
* You can use either `allowed_domains` or `blocked_domains`, but not both in the same request.

**Wildcard support:**

* Wildcards (`*`) are not allowed in the domain itself, only in the path after it.
* Valid: `example.com/*`, `example.com/*/articles`
* Invalid: `*.example.com`, `ex*.com`

Invalid domain formats are rejected at request time with a 400 `invalid_request_error`.

<Note>
  Request-level domain restrictions work together with any organization-level domain restrictions configured in Claude Console. Request-level `allowed_domains` must be a subset of the organization-level allowed list; entries outside it cause the API to return a validation error. A request-level allowed list that includes a domain your organization blocks is rejected with a `400` error that names the conflicting entries.
</Note>

<Warning>
  Unicode characters in domain names can bypass domain filters through homograph attacks: `аmazon.com` (with a Cyrillic `а`) looks identical to `amazon.com` but is a different domain. Use ASCII-only domain names in allow and block lists, and audit existing entries for non-ASCII characters.
</Warning>

[Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) uses the same `allowed_domains` and `blocked_domains` fields on the `web_search` and `web_fetch` entries of the agent toolset. On Managed Agents, each list holds at most 64 entries, domains listed for `web_fetch` cannot include a path, and fields specific to the Messages API tools, such as `max_uses`, `citations`, and `cache_control`, are not available. See [Domain list rules](https://platform.claude.com/docs/en/managed-agents/tools-web-restrictions#domain-list-rules) for the full rules.

Organization-level web search and web fetch settings in the Claude Console apply to Messages API requests only. They do not apply to Managed Agents sessions, which use the per-tool lists on the agent toolset instead. For a session in a cloud environment with `limited` networking, the environment's `allowed_hosts` also applies to `web_search` and `web_fetch`; see [Networking](https://platform.claude.com/docs/en/managed-agents/environments#networking). The per-tool lists restrict these tools further, within the hosts that `allowed_hosts` allows.

## Dynamic filtering with code execution

The `_20260209` and later versions of web search and web fetch use code execution internally to apply dynamic filters against search results.

<Note>
  You don't need to add a `code_execution` tool for these versions: when dynamic filtering runs, the API provisions code execution for the request automatically, and both tools share a single execution container. If you do include one, use `code_execution_20260120` or later; the API rejects older code execution versions alongside these web tool versions.
</Note>

## Streaming server-tool events

Server-tool events stream as part of the normal server-sent events (SSE) flow. A `server_tool_use` block that Claude calls directly streams like a client `tool_use` block: a `content_block_start` event followed by `input_json_delta` events. The result block arrives complete in a single `content_block_start` event, with no deltas.

See [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming) for the full event reference. Individual tool pages document tool-specific event names where they differ.

## Batch requests

All server tools support batch processing. In a batch, the agentic loop runs just as it does for synchronous requests, with a higher per-turn iteration limit. If the loop reaches that limit, the response ends with `stop_reason: "pause_turn"`; you can continue it by submitting a follow-up request with the returned content. See [Server tools and the agentic loop](https://platform.claude.com/docs/en/build-with-claude/batch-processing#server-tools-and-the-agentic-loop) for details.

Common batch workloads include enriching a dataset with information from the web, checking a large set of documents against current sources, and running analysis code over many files.

## Next steps

<CardGroup cols={2}>
  <Card title="Troubleshooting tool use" icon="wrench" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use">
    Fix the most common tool-use errors with symptom-to-fix diagnostic tables.
  </Card>

  <Card title="Web search tool" icon="magnifying-glass" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool">
    Search the web and cite results.
  </Card>

  <Card title="Web fetch tool" icon="download" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool">
    Fetch and read content from specific URLs to augment Claude's context with live web content.
  </Card>

  <Card title="Code execution tool" icon="terminal" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool">
    Run Python and bash code in a sandboxed container to analyze data, generate files, and iterate on solutions.
  </Card>

  <Card title="Tool search tool" icon="compass" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool">
    Discover and load tools on demand.
  </Card>
</CardGroup>

---
title: Thinking
url: https://platform.claude.com/docs/en/build-with-claude/thinking
description: "Understand how Claude's thinking works: turn it on, read thinking output, steer thinking depth with effort, and use thinking with tools, caching, and streaming."
---

<Note>
  To learn how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

A model that answers in a single pass has to get everything right on the first try: no scratch work, no checking, no changing course halfway through. For a proof, a tricky bug, or a long agentic task, the first approach is often not the best one.

Thinking removes that constraint. When thinking is active, Claude works through the problem in its own words before answering: it restates what is being asked, tries approaches, checks intermediate results, and abandons paths that do not hold up. That up-front thinking arrives in `thinking` content blocks ahead of the response, and Claude draws on it to produce the final answer. This is why thinking improves performance on complex tasks like math, coding, analysis, and long-running agentic work, where the quality of the answer depends on intermediate work that would otherwise be compressed into the response itself or skipped.

Thinking has a cost: the tokens Claude spends reasoning are billed as output tokens, even when the thinking text isn't returned to you, and they count toward `max_tokens` alongside the response text. This page covers how thinking behaves across the API surface: turning it on, reading its output, and managing its interactions with tools, streaming, caching, and the context window.

## How thinking works

<Frame>
  ![Diagram: Claude determines whether to think up front, may think between tool calls, and returns thinking blocks before text](https://platform.claude.com/docs/images/how-thinking-works.svg)
</Frame>

Whether Claude thinks on a given request, and how deeply, depends on your thinking configuration and the complexity of the request.

Here is what up-front thinking looks like in a response: one or more `thinking` content blocks arrive before the `text` blocks. The thinking block is still generated content, like the `text` block that follows it, but it is separated from the canonical response. Each thinking block also carries a `signature` field, an encrypted copy of the full reasoning that you pass back unchanged in multi-turn and tool-use conversations (see [Thinking encryption](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-encryption)):

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me break this down. The question has two parts, so I'll start with the simpler one and use its result to constrain the second...",
      "signature": "WaUjzkypQ2mUEVM36O2Txu...."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

You don't always see this text, and what you see is never the raw chain of thought: the text in a thinking block is a [summary of Claude's reasoning](https://platform.claude.com/docs/en/build-with-claude/thinking#summarized-thinking). The `display` field on the thinking configuration controls whether that summary is returned at all: `"summarized"` returns it, while `"omitted"`, the default on many models, returns thinking blocks with an empty `thinking` field. Either way the block is billed the same and passed back the same in multi-turn conversations. See [Controlling thinking display](https://platform.claude.com/docs/en/build-with-claude/thinking#controlling-thinking-display) for per-model defaults and details.

If Claude uses tools, thinking can also appear between tool calls. See [Thinking with tool use](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use). For the full response format, see the [Messages API reference](https://platform.claude.com/docs/en/api/messages/create).

## Configuring thinking

On most models, thinking is on by default or one parameter away. The following table shows what each model does with each `thinking` value a request can send. A 400 error means the API rejects the request, and [Troubleshooting thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting) has each error and its fix.

| Model                 | No `thinking` field | `"adaptive"`      | `"enabled"` with `budget_tokens` | `"between_tools"`                               | `"disabled"`                           |
| --------------------- | ------------------- | ----------------- | -------------------------------- | ----------------------------------------------- | -------------------------------------- |
| Claude Opus 5.5       | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | 400 error                              |
| Claude Sonnet 5.5     | Adaptive thinking   | Adaptive thinking | 400 error                        | Up-front thinking off at `high` effort or below | 400 error                              |
| Claude Haiku 5.5      | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | Thinking off at `high` effort or below |
| Claude Fable 5.1      | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | 400 error                              |
| Claude Mythos 5.1     | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | 400 error                              |
| Claude Fable 5        | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | 400 error                              |
| Claude Mythos 5       | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | 400 error                              |
| Claude Opus 5         | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | Thinking off at `high` effort or below |
| Claude Sonnet 5       | Adaptive thinking   | Adaptive thinking | 400 error                        | 400 error                                       | Thinking off                           |
| Claude Opus 4.8       | Thinking off        | Adaptive thinking | 400 error                        | 400 error                                       | Thinking off                           |
| Claude Opus 4.7       | Thinking off        | Adaptive thinking | 400 error                        | 400 error                                       | Thinking off                           |
| Claude Mythos Preview | Adaptive thinking   | Adaptive thinking | Extended thinking                | 400 error                                       | 400 error                              |
| Claude Opus 4.6       | Thinking off        | Adaptive thinking | Extended thinking (deprecated)   | 400 error                                       | Thinking off                           |
| Claude Sonnet 4.6     | Thinking off        | Adaptive thinking | Extended thinking (deprecated)   | 400 error                                       | Thinking off                           |
| Claude Opus 4.5       | Thinking off        | 400 error         | Extended thinking                | 400 error                                       | Thinking off                           |
| Claude Sonnet 4.5     | Thinking off        | 400 error         | Extended thinking                | 400 error                                       | Thinking off                           |
| Claude Haiku 4.5      | Thinking off        | 400 error         | Extended thinking                | 400 error                                       | Thinking off                           |

In the table, "at `high` effort or below" means the request works at `low`, `medium`, and `high` effort and returns a 400 error at `xhigh` or `max`.

On Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, and Claude Haiku 5.5, thinking is already on and needs no configuration. `display` defaults to `"omitted"` on these models, so the thinking text is hidden until you opt in. Opt in with `thinking: {"type": "adaptive", "display": "summarized"}`, which is exactly the following request with the [model string](https://platform.claude.com/docs/en/models/overview) swapped.

On Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6, thinking is off until you set `thinking: {type: "adaptive"}`, which lets Claude determine when and how deeply to think based on the request. The following examples do that, set `display: "summarized"` so the thinking text is visible, and use a roomy `max_tokens`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "thinking": {
        "type": "adaptive",
        "display": "summarized"
      },
      "messages": [
        {
          "role": "user",
          "content": "What is the greatest common divisor of 1071 and 462?"
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 16000 \
    --thinking '{type: adaptive, display: summarized}' \
    --message '{role: user, content: "What is the greatest common divisor of 1071 and 462?"}' \
    --transform content \
    --format yaml
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      thinking={"type": "adaptive", "display": "summarized"},
      messages=[
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?",
          }
      ],
  )

  for block in response.content:
      match block.type:
          case "thinking":
              print(f"\nThinking: {block.thinking}")
          case "text":
              print(f"\nResponse: {block.text}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: {
      type: "adaptive",
      display: "summarized"
    },
    messages: [
      {
        role: "user",
        content: "What is the greatest common divisor of 1071 and 462?"
      }
    ]
  });

  for (const block of response.content) {
    switch (block.type) {
      case "thinking":
        console.log(`\nThinking: ${block.thinking}`);
        break;
      case "text":
        console.log(`\nResponse: ${block.text}`);
        break;
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigAdaptive { Display = Display.Summarized },
      Messages = [
          new() {
              Role = Role.User,
              Content = "What is the greatest common divisor of 1071 and 462?"
          }
      ]
  };

  var message = await client.Messages.Create(parameters);

  foreach (var block in message.Content)
  {
      if (block.TryPickThinking(out ThinkingBlock? thinking))
      {
          Console.WriteLine($"\nThinking: {thinking.Thinking}");
      }
      else if (block.TryPickText(out TextBlock? text))
      {
          Console.WriteLine($"\nResponse: {text.Text}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
  			Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	switch v := block.AsAny().(type) {
  	case anthropic.ThinkingBlock:
  		fmt.Printf("\nThinking: %s", v.Thinking)
  	case anthropic.TextBlock:
  		fmt.Printf("\nResponse: %s", v.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ThinkingConfigAdaptive;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000L)
          .thinking(ThinkingConfigAdaptive.builder()
              .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
              .build())
          .addUserMessage("What is the greatest common divisor of 1071 and 462?")
          .build();

      Message response = client.messages().create(params);

      response.content().forEach(block -> {
          block.thinking().ifPresent(thinkingBlock ->
              IO.println("\nThinking: " + thinkingBlock.thinking())
          );
          block.text().ifPresent(textBlock ->
              IO.println("\nResponse: " + textBlock.text())
          );
      });
  }
  ```

  ```php PHP
  use Anthropic\Messages\TextBlock;
  use Anthropic\Messages\ThinkingBlock;

  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 16000,
      messages: [
          [
              'role' => 'user',
              'content' => 'What is the greatest common divisor of 1071 and 462?'
          ]
      ],
      model: 'claude-opus-4-8',
      thinking: ['type' => 'adaptive', 'display' => 'summarized'],
  );

  foreach ($message->content as $block) {
      switch (true) {
          case $block instanceof ThinkingBlock:
              echo "\nThinking: " . $block->thinking;
              break;
          case $block instanceof TextBlock:
              echo "\nResponse: " . $block->text;
              break;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: {
      type: "adaptive",
      # A plain hash like this one takes display:. The typed ThinkingConfigAdaptive class
      # spells it display_ (trailing underscore) to avoid shadowing Ruby's Kernel#display.
      # The request still sends display.
      display: "summarized"
    },
    messages: [
      {
        role: "user",
        content: "What is the greatest common divisor of 1071 and 462?"
      }
    ]
  )

  message.content.each do |block|
    case block
    when Anthropic::Models::ThinkingBlock
      puts "\nThinking: #{block.thinking}"
    when Anthropic::Models::TextBlock
      puts "\nResponse: #{block.text}"
    end
  end
  ```
</CodeGroup>

Running the example prints the summarized thinking, then the answer:

```text Output wrap
Thinking: Use Euclidean algorithm.
1071 = 2*462 + 147
462 = 3*147 + 21
147 = 7*21 + 0
GCD = 21

Response: ## Finding GCD of 1071 and 462

I'll use the **Euclidean algorithm**, repeatedly dividing and taking remainders...
```

Thinking tokens count toward `max_tokens`, so set it high enough to leave room for both the thinking and the response text. See [Cost control](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost#cost-control) on the steering page and [Thinking and the context window](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-the-context-window).

### Turning thinking off

On Claude Sonnet 5, where thinking is on by default, you can turn it off:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 4096,
      "thinking": {"type": "disabled"},
      "messages": [
        {
          "role": "user",
          "content": "Summarize this article in one sentence."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-sonnet-5 \
    --max-tokens 4096 \
    --thinking '{type: disabled}' \
    --message '{role: user, content: "Summarize this article in one sentence."}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=4096,
      thinking={"type": "disabled"},
      messages=[{"role": "user", "content": "Summarize this article in one sentence."}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 4096,
    thinking: { type: "disabled" },
    messages: [{ role: "user", content: "Summarize this article in one sentence." }]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 4096,
      Thinking = new ThinkingConfigDisabled(),
      Messages = [
          new() {
              Role = Role.User,
              Content = "Summarize this article in one sentence."
          }
      ]
  };

  var message = await client.Messages.Create(parameters);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5,
  	MaxTokens: 4096,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfDisabled: &anthropic.ThinkingConfigDisabledParam{},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize this article in one sentence.")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ThinkingConfigDisabled;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5)
          .maxTokens(4096L)
          .thinking(ThinkingConfigDisabled.builder().build())
          .addUserMessage("Summarize this article in one sentence.")
          .build();

      Message response = client.messages().create(params);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Summarize this article in one sentence.'
          ]
      ],
      model: 'claude-sonnet-5',
      thinking: ['type' => 'disabled'],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-5",
    max_tokens: 4096,
    thinking: { type: "disabled" },
    messages: [
      {
        role: "user",
        content: "Summarize this article in one sentence."
      }
    ]
  )
  ```
</CodeGroup>

Claude Opus 5 also has thinking on by default and accepts `thinking: {type: "disabled"}` at [effort](https://platform.claude.com/docs/en/build-with-claude/effort) `high` or below. At `xhigh` or `max` effort, thinking cannot be turned off: requests that combine `thinking: {type: "disabled"}` with those effort levels return a 400 error. This restriction is enforced on each request. With thinking disabled, Claude Opus 5 can occasionally emit tool calls as plain text or include internal XML tags in its visible output. See [Running with thinking disabled](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) for prompting mitigations.

Claude Sonnet 5.5 also has thinking on by default, and it rejects `thinking: {type: "disabled"}` with a 400 error. To turn off up-front thinking, send `thinking: {type: "between_tools"}` instead. It's the lowest thinking setting on Claude Sonnet 5.5, and it's accepted at [effort](https://platform.claude.com/docs/en/build-with-claude/effort) `high` or below. The model still returns its [progress updates between tool calls](https://platform.claude.com/docs/en/build-with-claude/thinking#progress-updates). Without tools, the response contains only text, as with `disabled` on Claude Sonnet 5. See [Running without up-front thinking](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#running-without-up-front-thinking) for prompting guidance.

Claude Haiku 5.5 also has thinking on by default and accepts `thinking: {type: "disabled"}` at [effort](https://platform.claude.com/docs/en/build-with-claude/effort) `high` or below. At `xhigh` or `max` effort, that combination returns a 400 error. To get less thinking, lower the effort level first. With thinking off, the model can skip a tool call it needs when you also request JSON output. See [Use effort to control thinking](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#use-effort-to-control-thinking) and [Use adaptive thinking with JSON output and your own tools](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#json-output-with-your-own-tools).

Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5, and Claude Mythos Preview reject `thinking: {type: "disabled"}`. Thinking can't be turned off on these models.

To check whether a model accepts `"disabled"` before you send a request, read its `capabilities.thinking.types.disabled.supported` value from the Models API. [Using the Models API](https://platform.claude.com/docs/en/models/overview#using-the-models-api) describes the field.

If your model supports only extended thinking (see the [per-model configuration table](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#supported-models)), configure it with `type: "enabled"` and a `budget_tokens` value instead. The [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) page covers that configuration. And if any thinking configuration comes back with a 400 error, [Troubleshooting thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting) matches each error message to its fix.

## Reading thinking output

### Controlling thinking display

The `display` field on the thinking configuration controls how thinking content is returned in API responses. `display` works in both modes: set it alongside `type: "adaptive"` or `type: "enabled"`. It accepts these values:

* `"summarized"`: thinking blocks contain [summarized thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#summarized-thinking) text, a readable summary of Claude's reasoning. This is the default on Claude Opus 4.6, Claude Sonnet 4.6, and earlier models.
* `"omitted"`: thinking blocks are returned with an empty `thinking` field. The `signature` field still carries the encrypted full thinking for multi-turn continuity (see [Thinking encryption](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-encryption)). This is the default on Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, [Claude Mythos Preview](https://anthropic.com/glasswing), and Claude Haiku 5.5.
* `"updates"` (beta): reasoning blocks are returned with an empty `thinking` field, as with `"omitted"`, and the short [progress updates](https://platform.claude.com/docs/en/build-with-claude/thinking#progress-updates) some models write between tool calls come back as readable text. Requires the beta header `thinking-display-updates-2026-08-18`.

Set `display: "omitted"` when your application doesn't surface thinking content to users. The primary benefit is faster time-to-first-text-token when streaming: the server skips streaming thinking tokens entirely and delivers only the signature, so the final text response begins streaming sooner.

With `display: "omitted"`, the response contains `thinking` blocks with an empty `thinking` field:

```json Output
{
  "content": [
    {
      "type": "thinking",
      "thinking": "",
      "signature": "EosnCkYICxIMMb3LzNrMu..."
    },
    {
      "type": "text",
      "text": "The answer is 12,231."
    }
  ]
}
```

Keep the following in mind when working with omitted thinking:

* You're still charged for the full thinking tokens. Omitting reduces latency, not cost.
* If you pass thinking blocks back in multi-turn conversations, pass them unchanged. The server decrypts the `signature` to reconstruct the original thinking for prompt construction (see [Preserving thinking blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#preserving-thinking-blocks)). Any text you place in the `thinking` field of a round-tripped omitted block is ignored.
* `display` is invalid with `thinking.type: "disabled"` (there is nothing to display).
* When using `thinking.type: "adaptive"` and the model skips thinking for a simple request, no thinking block is produced regardless of `display`.
* When streaming with `display: "omitted"`, no thinking text is streamed. Each thinking block streams a `thinking_delta` with an empty `thinking` string, then its `signature_delta`. With `display: "updates"`, only [progress-update blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#progress-updates) stream `thinking_delta` events that carry text. See [Streaming thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#streaming-thinking) for the event sequence.

<Note>
  The `signature` field is identical whichever `display` value you set. Switching `display` values between turns in a conversation is supported.
</Note>

### Summarized thinking

When `display` is `"summarized"`, the thinking text you receive is a summary of Claude's full thinking process rather than the raw chain of thought. Summarized thinking provides the full intelligence benefits of thinking while preventing misuse. No `display` setting returns the raw chain of thought.

Keep the following in mind when working with summarized thinking:

* You're charged for the full thinking tokens generated by the original request, not the summary tokens. The billed output token count does not match the count of tokens you see in the response.
* On Claude Opus 4.6, Claude Sonnet 4.6, and earlier models, the first few lines of thinking output are more verbose, providing detailed reasoning that's particularly helpful for prompt engineering purposes. [Claude Mythos Preview](https://anthropic.com/glasswing) summarizes from the first token, so its thinking blocks do not show this verbose preamble.
* Summarization preserves the key ideas of Claude's thinking process with minimal added latency, so summaries can stream as they arrive.
* Summarization is processed by a different model from the one you target in your requests. The thinking model does not see the summarized output.
* As Anthropic seeks to improve the thinking feature, summarization behavior is subject to change.

<Note>
  In rare cases where you need access to full thinking output, [contact Anthropic sales](mailto:sales@anthropic.com).
</Note>

To see the model's reasoning, read the `thinking` blocks rather than prompting for reasoning in the response text. On Claude Fable 5.1, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, and Claude Fable 5, a request that attempts to elicit the model's internal reasoning as part of the response text may be refused with `stop_details.category: "reasoning_extraction"`. See [Refusal categories](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response) for the field reference and [Keep reasoning in thinking blocks](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks) for what to ask for instead.

### Streaming thinking

Thinking works with [streaming](https://platform.claude.com/docs/en/build-with-claude/streaming). Thinking blocks stream as `thinking_delta` events inside `content_block_delta` events, followed by a single `signature_delta` event just before the block's `content_block_stop`. Text blocks stream afterward as usual.

<Frame>
  ![Diagram of the streaming event sequence with thinking: the thinking block opens, thinking deltas carry text only when the display setting returns text (summarized, or updates for progress-update blocks), a single signature delta closes the block, then text deltas stream](https://platform.claude.com/docs/images/how-thinking-streams.svg)
</Frame>

The following examples stream a response with adaptive thinking, printing thinking and text deltas as they arrive:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "stream": true,
      "thinking": {
        "type": "adaptive",
        "display": "summarized"
      },
      "messages": [
        {
          "role": "user",
          "content": "What is the greatest common divisor of 1071 and 462?"
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 16000 \
    --thinking '{type: adaptive, display: summarized}' \
    --message '{role: user, content: "What is the greatest common divisor of 1071 and 462?"}' \
    --stream \
    --format jsonl
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-4-8",
      max_tokens=16000,
      thinking={"type": "adaptive", "display": "summarized"},
      messages=[
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?",
          }
      ],
  ) as stream:
      for event in stream:
          match event.type:
              case "content_block_start":
                  print(f"\nStarting {event.content_block.type} block...")
              case "content_block_delta":
                  delta = event.delta
                  match delta.type:
                      case "thinking_delta":
                          print(delta.thinking, end="", flush=True)
                      case "text_delta":
                          print(delta.text, end="", flush=True)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: { type: "adaptive", display: "summarized" },
    messages: [{ role: "user", content: "What is the greatest common divisor of 1071 and 462?" }]
  });

  for await (const event of stream) {
    switch (event.type) {
      case "content_block_start":
        console.log(`\nStarting ${event.content_block.type} block...`);
        break;
      case "content_block_delta":
        switch (event.delta.type) {
          case "thinking_delta":
            process.stdout.write(event.delta.thinking);
            break;
          case "text_delta":
            process.stdout.write(event.delta.text);
            break;
        }
        break;
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigAdaptive { Display = Display.Summarized },
      Messages = [new() { Role = Role.User, Content = "What is the greatest common divisor of 1071 and 462?" }]
  };

  await foreach (var rawEvent in client.Messages.CreateStreaming(parameters))
  {
      if (rawEvent.TryPickContentBlockStart(out var start))
      {
          Console.WriteLine($"\nStarting {start.ContentBlock.Type} block...");
      }
      else if (rawEvent.TryPickContentBlockDelta(out var delta))
      {
          if (delta.Delta.TryPickThinking(out var thinkingDelta))
          {
              Console.Write(thinkingDelta.Thinking);
          }
          else if (delta.Delta.TryPickText(out var textDelta))
          {
              Console.Write(textDelta.Text);
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
  			Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockStartEvent:
  		fmt.Printf("\nStarting %s block...\n", eventVariant.ContentBlock.Type)
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.ThinkingDelta:
  			fmt.Print(deltaVariant.Thinking)
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ThinkingConfigAdaptive;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000L)
          .thinking(ThinkingConfigAdaptive.builder()
              .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
              .build())
          .addUserMessage("What is the greatest common divisor of 1071 and 462?")
          .build();

      try (var streamResponse = client.messages().createStreaming(params)) {
          streamResponse.stream().forEach(event -> {
              switch (event.type().value()) {
                  case CONTENT_BLOCK_START -> {
                      var startEvent = event.asContentBlockStart();
                      var block = startEvent.contentBlock();
                      switch (block.type().value()) {
                          case THINKING -> IO.println("\nStarting thinking block...");
                          case TEXT -> IO.println("\nStarting text block...");
                      }
                  }
                  case CONTENT_BLOCK_DELTA -> {
                      var deltaEvent = event.asContentBlockDelta();
                      deltaEvent.delta().thinking().ifPresent(td ->
                          IO.print(td.thinking())
                      );
                      deltaEvent.delta().text().ifPresent(td ->
                          IO.print(td.text())
                      );
                  }
              }
          });
      }
  }
  ```

  ```php PHP
  use Anthropic\Messages\RawContentBlockDeltaEvent;
  use Anthropic\Messages\RawContentBlockStartEvent;
  use Anthropic\Messages\TextDelta;
  use Anthropic\Messages\ThinkingDelta;

  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 16000,
      messages: [
          ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
      ],
      model: 'claude-opus-4-8',
      thinking: ['type' => 'adaptive', 'display' => 'summarized'],
  );

  foreach ($stream as $event) {
      switch (true) {
          case $event instanceof RawContentBlockStartEvent:
              echo "\nStarting {$event->contentBlock->type} block...\n";
              break;
          case $event instanceof RawContentBlockDeltaEvent:
              switch (true) {
                  case $event->delta instanceof ThinkingDelta:
                      echo $event->delta->thinking;
                      break;
                  case $event->delta instanceof TextDelta:
                      echo $event->delta->text;
                      break;
              }
              break;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    # A plain hash like this one takes display:. The typed ThinkingConfigAdaptive class
    # spells it display_ (trailing underscore) to avoid shadowing Ruby's Kernel#display.
    # The request still sends display.
    thinking: { type: "adaptive", display: "summarized" },
    messages: [
      { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
    ]
  )

  stream.each do |event|
    case event
    when Anthropic::Streaming::ThinkingEvent
      print event.thinking
    when Anthropic::Streaming::TextEvent
      print event.text
    end
  end
  ```
</CodeGroup>

To reassemble complete thinking blocks with their signatures after streaming, use your SDK's message-accumulation helper, `stream.get_final_message()` (typescript: `stream.finalMessage()`; ruby: `stream.accumulated_message`; csharp: `.Aggregate()`; go: `message.Accumulate(event)`; java, php: `MessageAccumulator`), instead of concatenating deltas yourself.

<Accordion title="Full streaming event trace">
  ```sse Output
  event: message_start
  data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-8", "stop_reason": null, "stop_sequence": null}}

  event: content_block_start
  data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": "", "signature": ""}}

  event: content_block_delta
  data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

  event: content_block_delta
  data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21\n147 = 7 × 21 + 0\n\nSo GCD(1071, 462) = 21"}}

  // Additional thinking deltas...

  event: content_block_delta
  data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b..."}}

  event: content_block_stop
  data: {"type": "content_block_stop", "index": 0}

  event: content_block_start
  data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

  event: content_block_delta
  data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "The greatest common divisor of 1071 and 462 is **21**."}}

  // Additional text deltas...

  event: content_block_stop
  data: {"type": "content_block_stop", "index": 1}

  event: message_delta
  data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

  event: message_stop
  data: {"type": "message_stop"}
  ```
</Accordion>

When `display: "omitted"` is set, the thinking block opens, a `thinking_delta` with an empty `thinking` string arrives, a single `signature_delta` follows, and the block closes. Text streaming begins immediately after:

```sse Output
event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"thinking","thinking":"","signature":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"thinking_delta","thinking":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"signature_delta","signature":"EosnCkYICxIMMb3LzNrMu..."}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"text","text":""}}
```

With `display: "updates"` (beta), reasoning blocks stream as they do under `"omitted"`. Each [progress-update block](https://platform.claude.com/docs/en/build-with-claude/thinking#progress-updates) streams its text as `thinking_delta` events before the `tool_use` block it introduces. A pause of several seconds before the progress-update block opens is normal:

```sse Output
event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"thinking","thinking":"","signature":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"thinking_delta","thinking":"Confirmed the retry path never refreshes the expired token. Editing auth.py to add the refresh call."}}

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"signature_delta","signature":"Es8CCkYICxIM..."}}

event: content_block_stop
data: {"type":"content_block_stop","index":1}

event: content_block_start
data: {"type":"content_block_start","index":2,"content_block":{"type":"tool_use","id":"toolu_01D7FLrfh4GYq7yT1ULFeyMV","name":"edit_file","input":{}}}
```

Under `"updates"`, treat a block as a progress update as soon as one of its `thinking_delta` events carries non-empty text.

<Note>
  When using streaming with thinking enabled, you might notice that text sometimes arrives in larger chunks alternating with smaller, token-by-token delivery. This is expected behavior, especially for thinking content.

  The streaming system processes content in batches, which can delay and group streaming events into this "chunky" delivery pattern.
</Note>

For general streaming mechanics, see [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming).

## Thinking and effort

The `thinking` parameter controls whether Claude thinks in [thinking blocks](https://platform.claude.com/docs/en/build-with-claude/thinking) before answering; the `effort` parameter controls how much work Claude puts into the whole response, which in adaptive mode includes how often and how deeply it thinks. Don't pass `adaptive` as an `effort` value: `adaptive` is a thinking mode, not an effort level.

To learn what each effort level does to thinking behavior, see the [per-level thinking behavior table](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost#effort-levels) on the [Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) page. The [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) page documents the parameter itself, including which levels each model supports. On Claude Opus 4.5, the only extended-thinking-only model that supports effort, effort composes with `budget_tokens`. See [Budget rules and tuning](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#budget-rules-and-tuning).

With the two controls separated this way, pick the one that matches your goal:

* **Lower cost or latency on a thinking-enabled workload:** lower `effort` first. It scales the whole response down, thinking included.
* **Claude is thinking too rarely or too shallowly:** raise `effort`, or see [Steering how often Claude thinks](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost#tuning-thinking-behavior) on the steering page.
* **You need thinking fully off:** use `thinking: {type: "disabled"}` on models that allow it (see the [per-model configuration table](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#supported-models)). Claude Sonnet 5.5 rejects `"disabled"`. Its lowest setting is `thinking: {type: "between_tools"}`, which turns off up-front thinking.
* **You need a hard ceiling on spend:** use `max_tokens`. Effort is soft guidance. `max_tokens` is a strict limit.

## Thinking with tool use

Thinking works alongside [tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), letting Claude reason through tool selection and process tool results. Two constraints apply:

1. **Tool choice limitation (manual mode):** tool use with manual extended thinking (`thinking: {type: "enabled"}`) only supports `tool_choice: {"type": "auto"}` (the default) or `tool_choice: {"type": "none"}`. Using `tool_choice: {"type": "any"}` or `tool_choice: {"type": "tool", "name": "..."}` results in an error because these options force tool use, which is incompatible with manual extended thinking. Adaptive thinking, including on models where thinking is on by default, supports forced tool use, except on Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 (see [Response prefill and forced tool use](https://platform.claude.com/docs/en/build-with-claude/thinking#limits-and-feature-compatibility)).
2. **Preserving thinking blocks:** when you return tool results, you must pass the thinking blocks from the assistant message back to the API, complete and unmodified. See [Preserving thinking blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#preserving-thinking-blocks).

**A tool-use loop is one assistant turn.** From the model's perspective, an assistant turn doesn't complete until Claude finishes its full response, which may include multiple tool calls and results. This whole sequence is a single assistant turn:

```text wrap
User: "What's the weather in Paris?"
Assistant: [thinking] + [tool_use: get_weather]
User: [tool_result: "20°C, sunny"]
Assistant: [text: "The weather in Paris is 20°C and sunny"]
```

The entire turn runs in a single thinking mode: you can't toggle thinking in the middle of a turn, including during the tool-use loop. In extended (manual) mode, the API additionally enforces that the final assistant turn of a thinking-enabled request begins with a thinking block. Adaptive mode relaxes this: no assistant turn needs to start with one.

**Mid-turn conflicts degrade gracefully.** If you toggle thinking mid-turn (for example, between sending a tool call and returning its result), the API doesn't error. Instead, it silently disables thinking for that request. To preserve model quality, the API may strip thinking blocks that would create an invalid turn structure, or disable thinking when the conversation history is incompatible with thinking being enabled. To confirm whether thinking was active, check for the presence of `thinking` blocks in the response.

**Toggle between turns, not within them.** Plan your thinking strategy at the start of each turn. Complete the assistant turn, then change the thinking configuration for the next one:

```text wrap
User: "What's the weather?"
Assistant: [tool_use] (thinking disabled)
User: [tool_result]
Assistant: [text: "It's sunny"]
User: "What about tomorrow?"
Assistant: [thinking] + [text: "..."] (thinking enabled - new turn)
```

Toggling thinking modes also invalidates prompt caching. See [Thinking and prompt caching](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-prompt-caching).

### Preserving thinking blocks

When Claude invokes a tool, it pauses construction of its response to await external information. When you return the tool result, Claude continues building that same response, so its earlier reasoning must still be present. Pass every `thinking` block back to the API complete and unmodified, alongside the `tool_use` block it accompanied. This matters for two reasons:

1. **Reasoning continuity:** the thinking blocks capture the step-by-step reasoning that led to the tool requests. Including them lets Claude continue reasoning from where it left off.
2. **Context maintenance:** tool results appear as user messages in the API structure, but they're part of one continuous reasoning flow. Preserving thinking blocks maintains that flow across API calls.

In short:

* **Required:** within a tool-use turn, pass thinking blocks back.
* **Recommended:** across turns, pass everything back.
* **Allowed:** outside tool use, omit prior turns' thinking.

You don't need to prune old thinking yourself. Pass all thinking blocks back in multi-turn conversations, and the API automatically filters them, keeps the blocks needed to preserve the model's reasoning, and bills input tokens only for the blocks actually shown to Claude. Which prior-turn blocks are kept is per-model. See [Thinking block preservation by model](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-block-preservation-by-model). To override the default, use the [`clear_thinking_20251015` context-editing strategy](https://platform.claude.com/docs/en/build-with-claude/context-editing#thinking-block-clearing).

Within the latest assistant message, the sequence of consecutive `thinking` blocks must match what the model generated in the original request: you can't rearrange, edit, or partially drop them. This includes [`redacted_thinking` blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#redacted-thinking-blocks).

<Note>
  Modified thinking blocks are rejected with a 400 error. See [A 400 error says thinking blocks cannot be modified](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#error-thinking-blocks-modified) for the exact message, the common causes, and the fix. The one exception: text placed in the empty `thinking` field of an [omitted](https://platform.claude.com/docs/en/build-with-claude/thinking#controlling-thinking-display) block is ignored rather than rejected.
</Note>

For a complete two-turn walkthrough with code in every SDK, see [Thinking in tool and multi-turn workflows](https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows#two-turn-tool-use-round-trip). It defines a tool, receives a thinking-plus-tool-use response, and echoes the assistant turn back with the tool result.

### Interleaved thinking

Interleaved thinking lets Claude think between tool calls, reasoning about each tool result before acting on it. With interleaved thinking, Claude can:

* Reason about the results of a tool call before determining what to do next
* Chain multiple tool calls with reasoning steps in between
* Make more nuanced decisions based on intermediate results

<Note>
  Consecutive tool calls do not require interleaved thinking. Claude can chain tool calls with or without interleaved thinking. Interleaving changes where thinking blocks appear between tool calls, not whether tool calls can chain.
</Note>

With adaptive thinking, interleaved thinking is automatic on every model that supports adaptive thinking. No beta header is needed. On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Opus 4.8, and Claude Opus 4.7, reasoning between tool calls always appears in thinking blocks. Claude Haiku 4.5 does not support interleaved thinking. On models using manual extended thinking, interleaving requires a beta header and changes how the thinking budget is counted. [Interleaved thinking in manual mode](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#interleaved-thinking) covers the per-model rules and platform-specific header behavior.

With interleaved thinking, the thinking allocation can span the entire assistant turn rather than a single response. Interleaved thinking is only supported for [tools used through the Messages API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

For a worked comparison showing what interleaved thinking changes in a two-tool workflow, see [How interleaved thinking changes the flow](https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows#how-interleaved-thinking-changes-the-flow).

### Progress updates between tool calls

On Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Sonnet 5.5, and Claude Fable 5, the model can write a progress update between tool calls. A progress update is a note on what the model just found and what it's about to do next, written for the person watching the agent rather than as reasoning. Each one comes back as its own `thinking` block with its own `signature`, separate from any reasoning block at the same point. It sits immediately before the `tool_use` or `server_tool_use` block it introduces. At most one progress update precedes each tool call, and the model can skip any of them. Progress updates aren't [interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#interleaved-thinking): they appear whether or not reasoning blocks appear between tool calls, and a response can contain both.

What a progress-update block contains depends on [`display`](https://platform.claude.com/docs/en/build-with-claude/thinking#controlling-thinking-display):

| `display`                                 | Reasoning blocks       | Progress-update blocks                                   |
| ----------------------------------------- | ---------------------- | -------------------------------------------------------- |
| `"omitted"` (the default on these models) | Empty `thinking` field | Empty `thinking` field                                   |
| `"updates"` (beta)                        | Empty `thinking` field | Summary text                                             |
| `"summarized"`                            | Summary text           | Summary text, not distinguishable from a reasoning block |

On Claude Sonnet 5.5, the lowest thinking setting is `thinking: {type: "between_tools"}`. It turns off up-front thinking, and each progress update comes back with its summary text, as it would under `display: "updates"`. `between_tools` is accepted only at [effort](https://platform.claude.com/docs/en/build-with-claude/effort) `high` or below. At `xhigh` or `max`, a request with it returns a 400 error. `between_tools` takes no other field: `display`, `budget_tokens`, or `block_binding` sent with it returns a 400 error. The setting needs no beta header and works on every platform that offers Claude Sonnet 5.5. Pass the blocks back unchanged: a progress-update block you send back gives the model the full note it wrote, not the summary.

Use `display: "updates"` for an agent interface that keeps reasoning hidden and shows the user a status line at each step. Under it, any `thinking` block with non-empty text is a progress update, so render those and nothing else. It's in beta and requires the beta header `thinking-display-updates-2026-08-18` (to send it on Amazon Bedrock, Google Cloud, or Microsoft Foundry, see [Beta features on other platforms](https://platform.claude.com/docs/en/api/beta-headers#beta-features-on-other-platforms)). Without it, the value is rejected with the same 400 `invalid_request_error` as an unknown `display` value.

```json
{
  "model": "claude-fable-5-1",
  "max_tokens": 16000,
  "thinking": { "type": "adaptive", "display": "updates" },
  "tools": [
    {
      "name": "edit_file",
      "description": "Replace the contents of a file in the repository.",
      "input_schema": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "content": { "type": "string" }
        },
        "required": ["path", "content"]
      }
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": "The login test fails after an hour of uptime. Find out why and fix it."
    }
  ]
}
```

Under `"updates"`, the start of the response that follows a `tool_result` looks like this. The first block is reasoning and stays empty, as it would under `"omitted"`. The second carries text, so it's a progress update. Under `"summarized"` both blocks carry text, and under `"omitted"` both are empty.

```json Output
{
  "content": [
    {
      "type": "thinking",
      "thinking": "",
      "signature": "EqMBCkYICxIM..."
    },
    {
      "type": "thinking",
      "thinking": "Confirmed the retry path never refreshes the expired token. Editing auth.py to add the refresh call.",
      "signature": "Es8CCkYICxIM..."
    },
    {
      "type": "tool_use",
      "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
      "name": "edit_file",
      "input": { "path": "auth.py", "content": "..." }
    }
  ]
}
```

Keep the following in mind when working with progress updates:

* Pass progress-update blocks back unchanged with the rest of the assistant turn, like any other `thinking` block.
* The text you receive is a summary of the progress update, normally a sentence or two. Don't rely on its length. The progress update counts toward `usage.output_tokens` at its full length, not the summary's.
* A progress-update block can come back with an empty `thinking` field under any `display` value. Render nothing for an empty block. Under `"updates"` it looks the same as an empty reasoning block and needs no separate handling.
* When a response stops on `max_tokens`, `model_context_window_exceeded`, or `stop_sequence` soon after a tool call or tool result, its last block can be a progress-update block standing in for the work the model hadn't finished. Under `"updates"` and `"summarized"` its text is exactly `This part of the response was interrupted before it finished.` and you can show it like any other update. Under `"omitted"` it's empty. To continue, pass the assistant turn back unchanged and append a new `user` message (with a `tool_result` for each `tool_use` block in that turn).
* When [streaming](https://platform.claude.com/docs/en/build-with-claude/thinking#streaming-thinking), expect a pause of several seconds before a progress-update block opens. See the `"updates"` trace in [Streaming thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#streaming-thinking).
* These models write fewer progress updates at higher [effort](https://platform.claude.com/docs/en/build-with-claude/effort) and in long tool chains. If your interface depends on them, see [Ask for user-facing progress updates](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#ask-for-user-facing-progress-updates) or, for Claude Opus 5.5, [User-facing progress updates](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#user-facing-progress-updates). For Claude Sonnet 5.5, see [User-facing progress updates](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#user-facing-progress-updates).

### Thinking block preservation by model

Whether thinking blocks from previous assistant turns stay in context by default depends on the model:

* **Keep all prior turns:** Claude Opus 4.5 and later Opus models, Claude Sonnet 4.6 and later Sonnet models, Claude Haiku 5.5, Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, and Claude Mythos Preview.
* **Keep the last turn only:** earlier Opus and Sonnet models, and all Haiku models through Claude Haiku 4.5. When you pass older thinking blocks back, the API strips them automatically. You don't need to remove them yourself.

Preservation brings two benefits:

* **Cache optimization:** preserved thinking blocks enable cache hits during tool use, as they are passed back with tool results and cached incrementally across the assistant turn, resulting in token savings in multistep workflows.
* **No intelligence impact:** preserving thinking blocks has no negative effect on model performance.

The tradeoff is context usage: long conversations consume more context space on keep-all models, because retained thinking blocks count as input like any other conversation history (see [Thinking and the context window](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-the-context-window)). The behavior is automatic in both regimes. No code changes or beta headers are required, and you should keep passing complete, unmodified thinking blocks back as described in [Preserving thinking blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#preserving-thinking-blocks). To override the default in either direction, use [thinking block clearing](https://platform.claude.com/docs/en/build-with-claude/context-editing#thinking-block-clearing).

**Switching models mid-conversation.** Keep passing thinking blocks back unchanged when you switch models, for example after a [classifier refusal fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback). A thinking block is readable only by the model that produced it and certain other models, and the API ignores or drops the blocks the target model can't read. On Claude Fable 5.1 and Claude Mythos 5.1 the direction matters: they read every earlier model's thinking blocks and no earlier model reads theirs, so switching up to them keeps the conversation's reasoning and switching down drops it (see [how dropped blocks are billed and reported](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#switching-models)). Claude Opus 5.5 reads Claude Opus 5's thinking blocks and those of earlier Opus, Sonnet, and Haiku models, and, on the Claude API and Google Cloud, of Claude Haiku 5.5, but not those of the Claude Fable and Claude Mythos models; on the Claude API, Claude Fable 5.1 and Claude Mythos 5.1 read Claude Opus 5.5's blocks. A switch from Claude Opus 5.5 up to Claude Fable 5.1 on the Claude API keeps the earlier turns' reasoning; a switch from Claude Fable 5.1 to Claude Opus 5.5 drops it. Claude Sonnet 5.5 reads thinking blocks from Claude Sonnet 5, Claude Opus 4.8, Claude Haiku 4.5, and earlier models, and, on the Claude API and Google Cloud, from Claude Haiku 5.5, but not from Claude Opus 5, Claude Opus 5.5, or any Claude Fable or Claude Mythos model. On the Claude API and Google Cloud, Claude Opus 5.5 reads Claude Sonnet 5.5's blocks and no other model does: a switch from Claude Sonnet 5.5 up to Claude Opus 5.5 on the Claude API and Google Cloud keeps the earlier turns' reasoning, and any other switch away from Claude Sonnet 5.5 drops it. Strip prior `thinking` and `redacted_thinking` blocks yourself only to save input tokens on models that ignore rather than drop them, and never when redeeming a [fallback credit](https://platform.claude.com/docs/en/build-with-claude/fallback-credit), which requires the body unchanged.

## Preserved thinking

[Preserved thinking](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking) determines whether the model can use a thinking block that you send back from an earlier turn. Starting with Claude Fable 5.1, the API checks the `signature` of every `thinking` or `redacted_thinking` block in a request for two things:

* **The model that produced it.** Each model reads its own thinking blocks and those of a fixed set of other models. Claude Fable 5.1 reads blocks from Claude Opus 5 and, on the Claude API, from Claude Opus 5.5; neither Claude Opus 5 nor Claude Opus 5.5 reads blocks from Claude Fable 5.1. The API drops a block the current model can't read, without an error and without billing it. See [Switching models mid-conversation](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#switching-models).
* **Everything sent before it.** A block stays valid only while the top-level `system` prompt, the `tools`, and the messages before it are unchanged. If any of them changes, that block and every later thinking block are invalid, and the API rejects the request with a 400 error or drops the invalid blocks, whichever you choose. See [Keeping the prefix unchanged](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#prefix-check).

Thinking blocks from Claude Sonnet 5.5 and Claude Haiku 5.5 are also tied to the account that produced them. See [Thinking blocks stay with the account that produced them](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#account-bound-thinking) for where the API enforces this.

The model check applies to every account. The API enforces the prefix check by default for accounts created on or after August 31, 2026, 00:00 UTC. On older accounts it enforces the check only on requests that set `thinking.block_binding.prefix_mismatch_behavior`. Make your integration append-only regardless of your account's age, so the same code works on every account, including newer accounts enforced by default.

To keep thinking valid, send every assistant turn back exactly as you received it and add new messages only at the end of `messages`. If your code builds the `messages` array itself, the Preserved thinking page covers:

* [What counts as an edit](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#what-counts-as-an-edit), and [how to check whether your code makes one](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#how-to-tell-whether-your-integration-is-impacted).
* [The API feature that replaces each common edit](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#replace-prefix-edits): mid-conversation system messages for new instructions and per-turn reminders, `tool_addition` and `tool_removal` blocks for tool changes, per-message `output_config` for effort changes, and server-side compaction and context editing for trimming.
* [Client-side compaction](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#custom-compaction-on-the-client): which patterns keep thinking valid and which don't.
* [The `thinking-binding-controls-2026-08-01` beta header](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking#preserved-thinking-controls). It adds a `block_binding.prefix_mismatch_behavior` field (`"error"` or `"drop_block"`) to the thinking configuration and an `input_transformations` array to every response. The array lists each thinking block that the API dropped, or that failed the prefix check and was let through.

## Thinking and prompt caching

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) interacts with thinking in a few specific ways. The following rules apply in both thinking modes.

**Configuration changes invalidate caching.** The thinking configuration and the resolved [`effort`](https://platform.claude.com/docs/en/build-with-claude/effort) level are rendered into the prompt itself, so changing any of them starts a new cache prefix. Switching between `adaptive`, `enabled`, and `disabled`, changing `budget_tokens`, and changing the effort value all invalidate cache breakpoints: message-level breakpoints always miss, and tool and system-prompt breakpoints can miss too, depending on where the model renders the configuration. Treat any thinking or top-level effort change as starting the cache over. On models that support [per-message effort](https://platform.claude.com/docs/en/build-with-claude/effort#change-effort-mid-conversation-beta), an effort change carried in a `role: "system"` message inside `messages` leaves the cached prefix intact. Consecutive requests that keep the same configuration preserve the cache, and setting a parameter explicitly to its default value is equivalent to omitting it. A thinking block the API drops under any [preserved-thinking condition](https://platform.claude.com/docs/en/build-with-claude/thinking#preserved-thinking) changes the cached prefix from that block's position onward. Blocks passed back unchanged keep the cache intact. A worked demonstration with usage output is on the [Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost#prompt-caching) page.

**Thinking blocks are cached with tool results.** During a tool-use loop, caching occurs when you make a follow-up request that includes tool results. At that point the previous conversation history, including its thinking blocks, can be cached, and those cached thinking blocks count as input tokens in your usage metrics when read from the cache. This occurs automatically, even without explicit `cache_control` markers, and behaves the same for regular and interleaved thinking. The tradeoff: thinking blocks you never see again in responses still contribute to input token usage when read from cache.

**Whether prior blocks are in context at all is per-model.** The [preservation default](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-block-preservation-by-model) governs this. On keep-all models, previous turns' thinking blocks stay cached and in context. On last-turn-only models, once you send a user message that isn't a tool result, all previous thinking blocks are stripped from context. On those models, a conversation like this:

```text wrap
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
```

is processed as if the thinking blocks were never there:

```text wrap
User: ["What's the weather in Paris?"],
Assistant: [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [text block 2],
User: [Text response, cache=True]
```

On keep-all models, the same request keeps `thinking_block_1` and `thinking_block_2` in context and in the cache.

**Degradation strips thinking from the cacheable history.** If thinking becomes disabled mid-turn and you pass thinking content in the current tool-use turn, the thinking content is stripped and thinking remains disabled for that request (see [graceful degradation](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use)). [Interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#interleaved-thinking) amplifies cache invalidation effects, because thinking blocks can occur between multiple tool calls.

<Tip>
  Thinking-heavy tasks often take longer than the default 5-minute cache lifetime to complete. Consider the [1-hour cache duration](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration) to maintain cache hits across longer thinking sessions and multistep workflows.
</Tip>

## Thinking and the context window

`max_tokens`, which includes all thinking Claude generates in the current turn, is enforced as a strict limit. On Claude 4.5 models and newer, if input tokens plus `max_tokens` exceeds the context window size, the API accepts the request. If generation then reaches the context window limit, it stops with `stop_reason: "model_context_window_exceeded"` instead of returning an error. On earlier models, the API returns a validation error instead. See [Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons).

How thinking counts against the window depends on when it was generated:

* **Current-turn thinking** always counts toward `max_tokens`, is billed as output tokens, and occupies context window space for the turn that generated it.
* **Prior-turn thinking** depends on the [preservation default](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-block-preservation-by-model). On [models that keep all prior turns](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-block-preservation-by-model), previous thinking blocks remain in context, count toward the window, and are billed as input tokens like the rest of the conversation history. On models that keep only the last turn, the API strips older thinking blocks automatically when you pass them back, so they don't consume window space or input tokens.

In practice:

* On keep-all models, budget your context window as if thinking were ordinary conversation history, because it is. Long agentic sessions accumulate thinking in context. Use [thinking block clearing](https://platform.claude.com/docs/en/build-with-claude/context-editing#thinking-block-clearing) if you need to reclaim space.
* On last-turn-only models, thinking is a per-turn cost only: each turn's thinking counts against that turn's `max_tokens` and then drops out of the window.

The following diagrams illustrate the last-turn-only (stripping) regime. The first shows a multi-turn conversation: each turn's thinking block is generated in the output but not carried into later turns' input.

<Frame>
  ![Diagram of thinking on a model that strips previous thinking blocks: each turn's thinking block is generated in the output and not carried into later turns' input](https://platform.claude.com/docs/images/context-window-thinking.svg)
</Frame>

The second shows the same regime with tool use: thinking stays in context alongside its tool result for the duration of the assistant turn, then drops out on the next user turn.

<Frame>
  ![Diagram of thinking with tool use on a model that strips previous thinking blocks: thinking is kept with its tool result, then dropped on the next user turn](https://platform.claude.com/docs/images/context-window-thinking-tools.svg)
</Frame>

Use the [token counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting) to get accurate counts for your specific use case, especially for multi-turn conversations that include thinking.

## Thinking encryption

Full thinking content is encrypted and returned in the `signature` field on each thinking block. The API uses the signature to verify that thinking blocks were generated by Claude when you pass them back.

Keep the following in mind when working with signatures:

* It is only strictly necessary to send back thinking blocks when [using tools with thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use). Otherwise you can omit thinking blocks from previous turns. If you do pass them back, whether the API keeps or strips them depends on the model (see [Thinking block preservation by model](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-block-preservation-by-model)). Use [context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) to configure this.
* When sending back thinking blocks, pass everything back exactly as you received it, for consistency and to avoid potential issues.
* When [streaming responses](https://platform.claude.com/docs/en/build-with-claude/thinking#streaming-thinking), the signature arrives as a `signature_delta` inside a `content_block_delta` event just before the `content_block_stop` event.
* `signature` values are significantly longer in Claude 4 and later models than in previous models.
* The `signature` field is opaque: don't interpret or parse it.
* `signature` values are compatible across platforms (the Claude API, [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock), and [Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)). Values generated on one platform work on another.

## Redacted thinking blocks

In addition to regular `thinking` blocks, the API may return `redacted_thinking` blocks when portions of Claude's reasoning are safety-redacted. A `redacted_thinking` block contains encrypted thinking content in a `data` field, with no readable text:

```json
{
  "type": "redacted_thinking",
  "data": "..."
}
```

The `data` field is opaque and encrypted. Like the `signature` field on regular thinking blocks, pass `redacted_thinking` blocks back to the API unchanged when continuing a multi-turn conversation with [tools](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use).

<Tip>
  If your code filters content blocks by type (for example, `block.type == "thinking"`) when round-tripping responses with tool use, also include `redacted_thinking` blocks. Filtering on `block.type == "thinking"` alone silently drops `redacted_thinking` blocks and breaks the multi-turn protocol described in [Preserving thinking blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#preserving-thinking-blocks).
</Tip>

<Note>
  `redacted_thinking` blocks are a distinct content block type returned when thinking is safety-redacted. This is separate from the [`display: "omitted"`](https://platform.claude.com/docs/en/build-with-claude/thinking#controlling-thinking-display) option, which returns regular `thinking` blocks with an empty `thinking` field.
</Note>

## Limits and feature compatibility

### Sampling parameters

On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5.5, Claude Sonnet 5, and Claude Haiku 5.5, non-default `temperature`, `top_p`, or `top_k` values return a 400 error on every request, regardless of whether thinking is used. On older models, the restriction applies only while thinking is on: `temperature` and `top_k` are incompatible with thinking, and `top_p` is allowed at values between 0.95 and 1.

### Response prefill and forced tool use

You can't prefill the assistant response while thinking is on. Forced tool use (`tool_choice: {"type": "any"}` or `{"type": "tool", ...}`) is incompatible with manual extended thinking but works with adaptive thinking. The exceptions are Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1, which reject forced tool use on every request with a 400 error. On those models, use `tool_choice: {"type": "auto"}` with [strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use) or [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) instead. See [Thinking with tool use](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use).

### Output limits

Each model accepts `max_tokens` up to the ceiling listed here. On the [Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing#extended-output-beta), the `output-300k-2026-03-24` [beta header](https://platform.claude.com/docs/en/api/beta-headers) raises that ceiling for the models with a batches ceiling listed.

| Model                 | Max output tokens | Batches beta ceiling |
| :-------------------- | :---------------- | :------------------- |
| Claude Fable 5.1      | 128K              | —                    |
| Claude Mythos 5.1     | 128K              | —                    |
| Claude Fable 5        | 128K              | —                    |
| Claude Mythos 5       | 128K              | —                    |
| Claude Mythos Preview | 128K              | Not available        |
| Claude Opus 5.5       | 128K              | 300K                 |
| Claude Opus 5         | 128K              | 300K                 |
| Claude Opus 4.8       | 128K              | 300K                 |
| Claude Opus 4.7       | 128K              | 300K                 |
| Claude Opus 4.6       | 128K              | 300K                 |
| Claude Opus 4.5       | 64K               | Not available        |
| Claude Sonnet 5.5     | 128K              | 300K                 |
| Claude Sonnet 5       | 128K              | 300K                 |
| Claude Sonnet 4.6     | 128K              | 300K                 |
| Claude Sonnet 4.5     | 64K               | Not available        |
| Claude Haiku 5.5      | 128K              | 300K                 |
| Claude Haiku 4.5      | 64K               | Not available        |

See the [models overview](https://platform.claude.com/docs/en/models/overview) for limits on legacy models.

### Long requests

The SDK requires streaming when `max_tokens` is greater than 21,333, to avoid HTTP timeouts on long-running requests. This is a client-side validation, not an API restriction. If you don't need to process events incrementally, use `.stream()` (java: `.createStreaming()`; csharp: `.CreateStreaming()`; go: `.NewStreaming()`; php: `->createStream()`) with `.get_final_message()` (typescript: `.finalMessage()`; ruby: `.accumulated_message`; csharp: `.Aggregate()`; go: `message.Accumulate(event)`; java, php: `MessageAccumulator`) to get the complete `Message` object without assembling it from individual events yourself. See [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming#get-the-final-message-without-handling-events). Expect longer response times when thinking is active, because generating thinking blocks adds processing time. For workloads that push thinking above roughly 32k tokens per request, use [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) to avoid networking issues: such requests can run long enough to hit system timeouts and open connection limits.

## Next steps

<CardGroup cols={2}>
  <Card title="Steering thinking" icon="compass" href="https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost">
    Steer how often and how deeply Claude thinks with effort levels, system prompt guidance, and per-message steering, and understand thinking's cost and pricing.
  </Card>

  <Card title="Thinking in tool and multi-turn workflows" icon="wrench" href="https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows">
    Walk through a complete two-turn tool-use round trip that preserves thinking blocks correctly, and see how interleaved thinking changes the flow.
  </Card>

  <Card title="Preserved thinking" icon="stack" href="https://platform.claude.com/docs/en/build-with-claude/preserved-thinking">
    Find out whether your Messages API integration edits conversation history, and replace each edit with the API feature that keeps earlier thinking blocks valid.
  </Card>

  <Card title="Troubleshooting thinking" icon="hammer" href="https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting">
    Diagnose and fix the most common thinking failures: configuration 400 errors, empty or missing thinking blocks, max\_tokens stops, and cache misses.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/en/build-with-claude/effort">
    Control how many tokens Claude uses when responding with the effort parameter, trading off between response thoroughness and token efficiency.
  </Card>
</CardGroup>


---
title: "Tutorial: Build a tool-using agent"
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent
description: A guided walkthrough from a single tool call to a production-ready agentic loop.
---

This tutorial builds a calendar-management agent in five concentric rings. Each ring is a complete, runnable program that adds exactly one concept to the ring before it. By the end you will have written the agentic loop by hand and then replaced it with the Tool Runner SDK abstraction.

The example tool is `create_calendar_event`. Its schema uses nested objects, arrays, and optional fields, so you will see how Claude handles realistic input shapes rather than a single flat string.

<Note>
  Every ring runs standalone. Copy any ring into a fresh file and it will run without the code from earlier rings.
</Note>

## Ring 1: Single tool, single turn

The smallest possible tool-using program: one tool, one user message, one tool call, one result. The code is heavily commented so you can map each line to the [tool use lifecycle](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works).

The request sends a `tools` array alongside the user message. When Claude determines that a tool call is needed, the response comes back with `stop_reason: "tool_use"` and a `tool_use` content block containing the tool name, a unique `id`, and the structured `input`. Your code runs the tool, then sends the result back in a `tool_result` block whose `tool_use_id` matches the `id` from the call.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 1: Single tool, single turn.

  # Define one tool as a JSON fragment. The input_schema is a JSON Schema
  # object describing the arguments Claude should pass when it calls this
  # tool. This schema includes nested objects (recurrence), arrays
  # (attendees), and optional fields, which is closer to real-world tools
  # than a flat string argument.
  TOOLS='[
    {
      "name": "create_calendar_event",
      "description": "Create a calendar event with attendees and optional recurrence.",
      "input_schema": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "start": {"type": "string", "format": "date-time"},
          "end": {"type": "string", "format": "date-time"},
          "attendees": {
            "type": "array",
            "items": {"type": "string", "format": "email"}
          },
          "recurrence": {
            "type": "object",
            "properties": {
              "frequency": {"enum": ["daily", "weekly", "monthly"]},
              "count": {"type": "integer", "minimum": 1}
            }
          }
        },
        "required": ["title", "start", "end"]
      }
    }
  ]'

  USER_MSG="Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am."

  # Send the user's request along with the tool definition. Claude decides
  # whether to call the tool based on the request and the tool description.
  RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n \
      --argjson tools "$TOOLS" \
      --arg msg "$USER_MSG" \
      '{
        model: "claude-opus-5-5",
        max_tokens: 1024,
        tools: $tools,
        tool_choice: {type: "auto", disable_parallel_tool_use: true},
        messages: [{role: "user", content: $msg}]
      }')")

  # When Claude calls a tool, the response has stop_reason "tool_use"
  # and the content array contains a tool_use block alongside any text.
  echo "stop_reason: $(echo "$RESPONSE" | jq -r '.stop_reason')"

  # Find the tool_use block. A response may contain text blocks before the
  # tool_use block, so filter by type rather than assuming position.
  TOOL_USE=$(echo "$RESPONSE" | jq '.content[] | select(.type == "tool_use")')
  TOOL_USE_ID=$(echo "$TOOL_USE" | jq -r '.id')
  echo "Tool: $(echo "$TOOL_USE" | jq -r '.name')"
  echo "Input: $(echo "$TOOL_USE" | jq -c '.input')"

  # Execute the tool. In a real system this would call your calendar API.
  # Here the result is hardcoded to keep the example self-contained.
  RESULT='{"event_id": "evt_123", "status": "created"}'

  # Send the result back. The tool_result block goes in a user message and
  # its tool_use_id must match the id from the tool_use block above. The
  # assistant's previous response is included so Claude has the full history.
  ASSISTANT_CONTENT=$(echo "$RESPONSE" | jq '.content')
  FOLLOWUP=$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$(jq -n \
      --argjson tools "$TOOLS" \
      --arg msg "$USER_MSG" \
      --argjson assistant "$ASSISTANT_CONTENT" \
      --arg tool_use_id "$TOOL_USE_ID" \
      --arg result "$RESULT" \
      '{
        model: "claude-opus-5-5",
        max_tokens: 1024,
        tools: $tools,
        tool_choice: {type: "auto", disable_parallel_tool_use: true},
        messages: [
          {role: "user", content: $msg},
          {role: "assistant", content: $assistant},
          {role: "user", content: [
            {type: "tool_result", tool_use_id: $tool_use_id, content: $result}
          ]}
        ]
      }')")

  # With the tool result in hand, Claude produces a final natural-language
  # answer and stop_reason becomes "end_turn".
  echo "stop_reason: $(echo "$FOLLOWUP" | jq -r '.stop_reason')"
  echo "$FOLLOWUP" | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 1: Single tool, single turn.
  # Uses jq for cross-turn message-array state — building an agentic loop in shell
  # requires JSON manipulation beyond ant's single-call --transform scope.
  set -euo pipefail

  USER_MSG="Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am."
  MESSAGES=$(jq -n --arg msg "$USER_MSG" '[{role: "user", content: $msg}]')

  # Define one tool. The input_schema is a JSON Schema object describing
  # the arguments Claude should pass when it calls this tool. This schema
  # includes nested objects (recurrence), arrays (attendees), and optional
  # fields, which is closer to real-world tools than a flat string argument.
  call_api() {
    # ant reads the request body as YAML on stdin: no auth headers, no
    # hand-built JSON envelope. The static keys (model, tools, tool_choice)
    # live in a quoted heredoc; the growing messages array is appended as
    # JSON, which YAML accepts as flow syntax.
    {
      cat <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tool_choice: {type: auto, disable_parallel_tool_use: true}
  tools:
    - name: create_calendar_event
      description: Create a calendar event with attendees and optional recurrence.
      input_schema:
        type: object
        properties:
          title: {type: string}
          start: {type: string, format: date-time}
          end: {type: string, format: date-time}
          attendees:
            type: array
            items: {type: string, format: email}
          recurrence:
            type: object
            properties:
              frequency: {enum: [daily, weekly, monthly]}
              count: {type: integer, minimum: 1}
        required: [title, start, end]
  YAML
      printf 'messages: %s\n' "$MESSAGES"
    } | ant messages create --format json
  }

  # Send the user's request along with the tool definition. Claude decides
  # whether to call the tool based on the request and the tool description.
  RESPONSE=$(call_api)

  # When Claude calls a tool, the response has stop_reason "tool_use"
  # and the content array contains a tool_use block alongside any text.
  echo "stop_reason: $(jq -r '.stop_reason' <<<"$RESPONSE")"

  # Find the tool_use block. A response may contain text blocks before the
  # tool_use block, so filter by type rather than assuming position.
  TOOL_USE=$(jq '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")
  TOOL_USE_ID=$(jq -r '.id' <<<"$TOOL_USE")
  echo "Tool: $(jq -r '.name' <<<"$TOOL_USE")"
  echo "Input: $(jq -c '.input' <<<"$TOOL_USE")"

  # Execute the tool. In a real system this would call your calendar API.
  # Here the result is hardcoded to keep the example self-contained.
  RESULT='{"event_id": "evt_123", "status": "created"}'

  # Send the result back. The tool_result block goes in a user message and
  # its tool_use_id must match the id from the tool_use block above. The
  # assistant's previous response is included so Claude has the full history.
  MESSAGES=$(jq \
    --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
    --arg tool_use_id "$TOOL_USE_ID" \
    --arg result "$RESULT" \
    '. + [
      {role: "assistant", content: $assistant},
      {role: "user", content: [
        {type: "tool_result", tool_use_id: $tool_use_id, content: $result}
      ]}
    ]' <<<"$MESSAGES")

  FOLLOWUP=$(call_api)

  # With the tool result in hand, Claude produces a final natural-language
  # answer and stop_reason becomes "end_turn".
  echo "stop_reason: $(jq -r '.stop_reason' <<<"$FOLLOWUP")"
  jq -r '.content[] | select(.type == "text") | .text' <<<"$FOLLOWUP"
  ```

  ```python Python
  # Ring 1: Single tool, single turn.

  import json

  import anthropic

  # Create a client. It reads ANTHROPIC_API_KEY from the environment.
  client = anthropic.Anthropic()

  # Define one tool. The input_schema is a JSON Schema object describing
  # the arguments Claude should pass when it calls this tool. This schema
  # includes nested objects (recurrence), arrays (attendees), and optional
  # fields, which is closer to real-world tools than a flat string argument.
  tools = [
      {
          "name": "create_calendar_event",
          "description": "Create a calendar event with attendees and optional recurrence.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "title": {"type": "string"},
                  "start": {"type": "string", "format": "date-time"},
                  "end": {"type": "string", "format": "date-time"},
                  "attendees": {
                      "type": "array",
                      "items": {"type": "string", "format": "email"},
                  },
                  "recurrence": {
                      "type": "object",
                      "properties": {
                          "frequency": {"enum": ["daily", "weekly", "monthly"]},
                          "count": {"type": "integer", "minimum": 1},
                      },
                  },
              },
              "required": ["title", "start", "end"],
          },
      }
  ]

  # Send the user's request along with the tool definition. Claude decides
  # whether to call the tool based on the request and the tool description.
  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=[
          {
              "role": "user",
              "content": "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.",
          }
      ],
  )

  # When Claude calls a tool, the response has stop_reason "tool_use"
  # and the content array contains a tool_use block alongside any text.
  print(f"stop_reason: {response.stop_reason}")

  # Find the tool_use block. A response may contain text blocks before the
  # tool_use block, so scan the content array rather than assuming position.
  tool_use = next(block for block in response.content if block.type == "tool_use")
  print(f"Tool: {tool_use.name}")
  print(f"Input: {tool_use.input}")

  # Execute the tool. In a real system this would call your calendar API.
  # Here the result is hardcoded to keep the example self-contained.
  result = {"event_id": "evt_123", "status": "created"}

  # Send the result back. The tool_result block goes in a user message and
  # its tool_use_id must match the id from the tool_use block above. The
  # assistant's previous response is included so Claude has the full history.
  followup = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=[
          {
              "role": "user",
              "content": "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.",
          },
          {"role": "assistant", "content": response.content},
          {
              "role": "user",
              "content": [
                  {
                      "type": "tool_result",
                      "tool_use_id": tool_use.id,
                      "content": json.dumps(result),
                  }
              ],
          },
      ],
  )

  # With the tool result in hand, Claude produces a final natural-language
  # answer and stop_reason becomes "end_turn".
  print(f"stop_reason: {followup.stop_reason}")
  final_text = next(block for block in followup.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 1: Single tool, single turn.

  import Anthropic from "@anthropic-ai/sdk";

  // Create a client. It reads ANTHROPIC_API_KEY from the environment.
  const client = new Anthropic();

  // Define one tool. The input_schema is a JSON Schema object describing
  // the arguments Claude should pass when it calls this tool. This schema
  // includes nested objects (recurrence), arrays (attendees), and optional
  // fields, which is closer to real-world tools than a flat string argument.
  const tools: Anthropic.Tool[] = [
    {
      name: "create_calendar_event",
      description:
        "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: { type: "string" },
          start: { type: "string", format: "date-time" },
          end: { type: "string", format: "date-time" },
          attendees: {
            type: "array",
            items: { type: "string", format: "email" },
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: { enum: ["daily", "weekly", "monthly"] },
              count: { type: "integer", minimum: 1 },
            },
          },
        },
        required: ["title", "start", "end"],
      },
    },
  ];

  // Send the user's request along with the tool definition. Claude decides
  // whether to call the tool based on the request and the tool description.
  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages: [
      {
        role: "user",
        content:
          "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.",
      },
    ],
  });

  // When Claude calls a tool, the response has stop_reason "tool_use"
  // and the content array contains a tool_use block alongside any text.
  console.log(`stop_reason: ${response.stop_reason}`);

  // Find the tool_use block. A response may contain text blocks before the
  // tool_use block, so scan the content array rather than assuming position.
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use",
  )!;
  console.log(`Tool: ${toolUse.name}`);
  console.log(`Input: ${JSON.stringify(toolUse.input)}`);

  // Execute the tool. In a real system this would call your calendar API.
  // Here the result is hardcoded to keep the example self-contained.
  const result = { event_id: "evt_123", status: "created" };

  // Send the result back. The tool_result block goes in a user message and
  // its tool_use_id must match the id from the tool_use block above. The
  // assistant's previous response is included so Claude has the full history.
  const followup = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages: [
      {
        role: "user",
        content:
          "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.",
      },
      { role: "assistant", content: response.content },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: toolUse.id,
            content: JSON.stringify(result),
          },
        ],
      },
    ],
  });

  // With the tool result in hand, Claude produces a final natural-language
  // answer and stop_reason becomes "end_turn".
  console.log(`stop_reason: ${followup.stop_reason}`);
  for (const block of followup.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  // Ring 1: Single tool, single turn.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  // Create a client. It reads ANTHROPIC_API_KEY from the environment.
  AnthropicClient client = new();

  // Define one tool. The input schema is a JSON Schema object describing
  // the arguments Claude should pass when it calls this tool. This schema
  // includes nested objects (recurrence), arrays (attendees), and optional
  // fields, which is closer to real-world tools than a flat string argument.
  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
  ];

  // Ask for at most one tool call per turn so the single-turn flow below
  // stays predictable.
  var toolChoice = new ToolChoice(new ToolChoiceAuto { DisableParallelToolUse = true });

  const string userPrompt =
      "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.";

  // Send the user's request along with the tool definition. Claude decides
  // whether to call the tool based on the request and the tool description.
  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages = [new() { Role = Role.User, Content = userPrompt }],
  });

  // When Claude calls a tool, the response has stop_reason "tool_use"
  // and the content array contains a tool_use block alongside any text.
  Console.WriteLine($"stop_reason: {response.StopReason?.Raw()}");

  // Find the tool_use block. A response may contain text blocks before the
  // tool_use block, so scan the content array rather than assuming position.
  ToolUseBlock? toolUse = null;
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var picked))
      {
          toolUse = picked;
          break;
      }
  }
  Console.WriteLine($"Tool: {toolUse!.Name}");
  Console.WriteLine($"Input: {JsonSerializer.Serialize(toolUse.Input)}");

  // Execute the tool. In a real system this would call your calendar API.
  // Here the result is hardcoded to keep the example self-contained.
  var result = """{"event_id": "evt_123", "status": "created"}""";

  // Send the result back. The tool_result block goes in a user message and
  // its tool_use_id must match the id from the tool_use block above. The
  // assistant's previous response is included so Claude has the full history.
  List<ContentBlockParam> toolResults =
  [
      new ContentBlockParam(new ToolResultBlockParam()
      {
          ToolUseID = toolUse.ID,
          Content = result,
      }),
  ];

  var followup = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages =
      [
          new() { Role = Role.User, Content = userPrompt },
          new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
          new() { Role = Role.User, Content = new MessageParamContent(toolResults) },
      ],
  });

  // With the tool result in hand, Claude produces a final natural-language
  // answer and stop_reason becomes "end_turn".
  Console.WriteLine($"stop_reason: {followup.StopReason?.Raw()}");
  foreach (var block in followup.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 1: Single tool, single turn.

  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	// Create a client. It reads ANTHROPIC_API_KEY from the environment.
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	// Define one tool. The input schema is a JSON Schema object describing
  	// the arguments Claude should pass when it calls this tool. This schema
  	// includes nested objects (recurrence), arrays (attendees), and optional
  	// fields, which is closer to real-world tools than a flat string argument.
  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  	}

  	// Ask for at most one tool call per turn so the single-turn flow below
  	// stays predictable.
  	toolChoice := anthropic.ToolChoiceUnionParam{
  		OfAuto: &anthropic.ToolChoiceAutoParam{DisableParallelToolUse: anthropic.Bool(true)},
  	}

  	userMessage := anthropic.NewUserMessage(anthropic.NewTextBlock(
  		"Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.",
  	))

  	// Send the user's request along with the tool definition. Claude decides
  	// whether to call the tool based on the request and the tool description.
  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus5_5,
  		MaxTokens:  1024,
  		Tools:      tools,
  		ToolChoice: toolChoice,
  		Messages:   []anthropic.MessageParam{userMessage},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// When Claude calls a tool, the response has stop_reason "tool_use"
  	// and the content array contains a tool_use block alongside any text.
  	fmt.Printf("stop_reason: %s\n", response.StopReason)

  	// Find the tool_use block. A response may contain text blocks before the
  	// tool_use block, so scan the content array rather than assuming position.
  	var toolUse anthropic.ContentBlockUnion
  	for _, block := range response.Content {
  		if block.Type == "tool_use" {
  			toolUse = block
  			break
  		}
  	}
  	fmt.Printf("Tool: %s\n", toolUse.Name)
  	fmt.Printf("Input: %s\n", string(toolUse.Input))

  	// Execute the tool. In a real system this would call your calendar API.
  	// Here the result is hardcoded to keep the example self-contained.
  	result := `{"event_id": "evt_123", "status": "created"}`

  	// Send the result back. The tool_result block goes in a user message and
  	// its tool_use_id must match the id from the tool_use block above. The
  	// assistant's previous response is included so Claude has the full history.
  	var assistantContent []anthropic.ContentBlockParamUnion
  	for _, block := range response.Content {
  		assistantContent = append(assistantContent, block.ToParam())
  	}

  	followup, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus5_5,
  		MaxTokens:  1024,
  		Tools:      tools,
  		ToolChoice: toolChoice,
  		Messages: []anthropic.MessageParam{
  			userMessage,
  			anthropic.NewAssistantMessage(assistantContent...),
  			anthropic.NewUserMessage(anthropic.NewToolResultBlock(toolUse.ID, result, false)),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// With the tool result in hand, Claude produces a final natural-language
  	// answer and stop_reason becomes "end_turn".
  	fmt.Printf("stop_reason: %s\n", followup.StopReason)
  	for _, block := range followup.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 1: Single tool, single turn.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolChoiceAuto;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.List;
  import java.util.Map;

  void main() {
      // Create a client. It reads ANTHROPIC_API_KEY from the environment.
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Define one tool. The input schema is a JSON Schema object describing
      // the arguments Claude should pass when it calls this tool. This schema
      // includes nested objects (recurrence), arrays (attendees), and optional
      // fields, which is closer to real-world tools than a flat string argument.
      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      // Ask for at most one tool call per turn so the single-turn flow below
      // stays predictable.
      ToolChoiceAuto toolChoice = ToolChoiceAuto.builder()
          .disableParallelToolUse(true)
          .build();

      String userPrompt =
          "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.";

      // Send the user's request along with the tool definition. Claude decides
      // whether to call the tool based on the request and the tool description.
      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .toolChoice(toolChoice)
          .addUserMessage(userPrompt)
          .build());

      // When Claude calls a tool, the response has stop_reason "tool_use"
      // and the content array contains a tool_use block alongside any text.
      IO.println("stop_reason: " + response.stopReason().orElse(null));

      // Find the tool_use block. A response may contain text blocks before the
      // tool_use block, so scan the content array rather than assuming position.
      ToolUseBlock toolUse = response.content().stream()
          .flatMap(block -> block.toolUse().stream())
          .findFirst()
          .orElseThrow();
      IO.println("Tool: " + toolUse.name());
      IO.println("Input: " + toolUse._input());

      // Execute the tool. In a real system this would call your calendar API.
      // Here the result is hardcoded to keep the example self-contained.
      String result = "{\"event_id\": \"evt_123\", \"status\": \"created\"}";

      // Send the result back. The tool_result block goes in a user message and
      // its tool_use_id must match the id from the tool_use block above. The
      // assistant's previous response is included so Claude has the full history.
      Message followup = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .toolChoice(toolChoice)
          .addUserMessage(userPrompt)
          .addMessage(response)
          .addUserMessageOfBlockParams(List.of(ContentBlockParam.ofToolResult(
              ToolResultBlockParam.builder()
                  .toolUseId(toolUse.id())
                  .content(result)
                  .build())))
          .build());

      // With the tool result in hand, Claude produces a final natural-language
      // answer and stop_reason becomes "end_turn".
      IO.println("stop_reason: " + followup.stopReason().orElse(null));
      followup.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 1: Single tool, single turn.

  use Anthropic\Client;
  use Anthropic\Messages\ToolChoiceAuto;

  // Create a client. It reads ANTHROPIC_API_KEY from the environment.
  $client = new Client();

  // Define one tool. The input_schema is a JSON Schema object describing
  // the arguments Claude should pass when it calls this tool. This schema
  // includes nested objects (recurrence), arrays (attendees), and optional
  // fields, which is closer to real-world tools than a flat string argument.
  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
  ];

  $userMessage = [
      'role' => 'user',
      'content' => 'Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am.',
  ];

  // Ask for at most one tool call per turn so the single-turn flow below
  // stays predictable.
  $toolChoice = ToolChoiceAuto::with(disableParallelToolUse: true);

  // Send the user's request along with the tool definition. Claude decides
  // whether to call the tool based on the request and the tool description.
  $response = $client->messages->create(
      model: 'claude-opus-5-5',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: [$userMessage],
  );

  // When Claude calls a tool, the response has stop_reason "tool_use"
  // and the content array contains a tool_use block alongside any text.
  printf("stop_reason: %s\n", $response->stopReason);

  // Find the tool_use block. A response may contain text blocks before the
  // tool_use block, so scan the content array rather than assuming position.
  $toolUse = null;
  foreach ($response->content as $block) {
      if ($block->type === 'tool_use') {
          $toolUse = $block;
          break;
      }
  }
  printf("Tool: %s\n", $toolUse->name);
  printf("Input: %s\n", json_encode($toolUse->input));

  // Execute the tool. In a real system this would call your calendar API.
  // Here the result is hardcoded to keep the example self-contained.
  $result = ['event_id' => 'evt_123', 'status' => 'created'];

  // Send the result back. The tool_result block goes in a user message and
  // its tool_use_id must match the id from the tool_use block above. The
  // assistant's previous response is included so Claude has the full history.
  $followup = $client->messages->create(
      model: 'claude-opus-5-5',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: [
          $userMessage,
          ['role' => 'assistant', 'content' => $response->content],
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => $toolUse->id,
                      'content' => json_encode($result),
                  ],
              ],
          ],
      ],
  );

  // With the tool result in hand, Claude produces a final natural-language
  // answer and stop_reason becomes "end_turn".
  printf("stop_reason: %s\n", $followup->stopReason);
  foreach ($followup->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 1: Single tool, single turn.

  require "anthropic"

  # Create a client. It reads ANTHROPIC_API_KEY from the environment.
  client = Anthropic::Client.new

  # Define one tool. The input_schema is a JSON Schema object describing
  # the arguments Claude should pass when it calls this tool. This schema
  # includes nested objects (recurrence), arrays (attendees), and optional
  # fields, which is closer to real-world tools than a flat string argument.
  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    }
  ]

  user_message = {
    role: "user",
    content: "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am."
  }

  # Ask for at most one tool call per turn so the single-turn flow below
  # stays predictable.
  tool_choice = {type: "auto", disable_parallel_tool_use: true}

  # Send the user's request along with the tool definition. Claude decides
  # whether to call the tool based on the request and the tool description.
  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: tools,
    tool_choice: tool_choice,
    messages: [user_message]
  )

  # When Claude calls a tool, the response has stop_reason "tool_use"
  # and the content array contains a tool_use block alongside any text.
  puts "stop_reason: #{response.stop_reason}"

  # Find the tool_use block. A response may contain text blocks before the
  # tool_use block, so scan the content array rather than assuming position.
  tool_use = response.content.find { |block| block.type == :tool_use }
  puts "Tool: #{tool_use.name}"
  puts "Input: #{tool_use.input}"

  # Execute the tool. In a real system this would call your calendar API.
  # Here the result is hardcoded to keep the example self-contained.
  result = {event_id: "evt_123", status: "created"}

  # Send the result back. The tool_result block goes in a user message and
  # its tool_use_id must match the id from the tool_use block above. The
  # assistant's previous response is included so Claude has the full history.
  followup = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: tools,
    tool_choice: tool_choice,
    messages: [
      user_message,
      {role: "assistant", content: response.content},
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: tool_use.id,
            content: JSON.generate(result)
          }
        ]
      }
    ]
  )

  # With the tool result in hand, Claude produces a final natural-language
  # answer and stop_reason becomes "end_turn".
  puts "stop_reason: #{followup.stop_reason}"
  followup.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**What to expect**

```text Output wrap
stop_reason: tool_use
Tool: create_calendar_event
Input: {'title': 'Sync', 'start': '2026-03-30T10:00:00', 'end': '2026-03-30T10:30:00', 'attendees': ['alice@example.com', 'bob@example.com']}
stop_reason: end_turn
I've scheduled your 30-minute sync with Alice and Bob for Monday, March 30 at 10am.
```

The first `stop_reason` is `tool_use` because Claude is waiting for the calendar result. After you send the result, the second `stop_reason` is `end_turn` and the content is natural language for the user.

## Ring 2: The agentic loop

Ring 1 assumed Claude would call the tool exactly once. Real tasks often need several calls: Claude might create an event, read the confirmation, then create another. The fix is a `while` loop that keeps running tools and feeding results back until `stop_reason` is no longer `"tool_use"`.

The other change is conversation history. Instead of rebuilding the `messages` array from scratch on each request, keep a running list and append to it. Every turn sees the complete prior context.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 2: The agentic loop.

  TOOLS='[
    {
      "name": "create_calendar_event",
      "description": "Create a calendar event with attendees and optional recurrence.",
      "input_schema": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "start": {"type": "string", "format": "date-time"},
          "end": {"type": "string", "format": "date-time"},
          "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
          "recurrence": {
            "type": "object",
            "properties": {
              "frequency": {"enum": ["daily", "weekly", "monthly"]},
              "count": {"type": "integer", "minimum": 1}
            }
          }
        },
        "required": ["title", "start", "end"]
      }
    }
  ]'

  run_tool() {
    local name="$1"
    local input="$2"
    if [ "$name" = "create_calendar_event" ]; then
      local title=$(echo "$input" | jq -r '.title')
      jq -n --arg title "$title" '{event_id: "evt_123", status: "created", title: $title}'
    else
      echo "{\"error\": \"Unknown tool: $name\"}"
    fi
  }

  # Keep the full conversation history in a JSON array so each turn sees prior context.
  MESSAGES='[{"role": "user", "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."}]'

  call_api() {
    curl -s https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d "$(jq -n --argjson tools "$TOOLS" --argjson messages "$MESSAGES" \
        '{model: "claude-opus-5-5", max_tokens: 1024, tools: $tools, tool_choice: {type: "auto", disable_parallel_tool_use: true}, messages: $messages}')"
  }

  RESPONSE=$(call_api)

  # Loop until Claude stops asking for tools. Each iteration runs the requested
  # tool, appends the result to history, and asks Claude to continue.
  while [ "$(echo "$RESPONSE" | jq -r '.stop_reason')" = "tool_use" ]; do
    TOOL_USE=$(echo "$RESPONSE" | jq '.content[] | select(.type == "tool_use")')
    TOOL_NAME=$(echo "$TOOL_USE" | jq -r '.name')
    TOOL_INPUT=$(echo "$TOOL_USE" | jq -c '.input')
    TOOL_USE_ID=$(echo "$TOOL_USE" | jq -r '.id')
    RESULT=$(run_tool "$TOOL_NAME" "$TOOL_INPUT")

    ASSISTANT_CONTENT=$(echo "$RESPONSE" | jq '.content')
    MESSAGES=$(echo "$MESSAGES" | jq \
      --argjson assistant "$ASSISTANT_CONTENT" \
      --arg tool_use_id "$TOOL_USE_ID" \
      --arg result "$RESULT" \
      '. + [
        {role: "assistant", content: $assistant},
        {role: "user", content: [{type: "tool_result", tool_use_id: $tool_use_id, content: $result}]}
      ]')

    RESPONSE=$(call_api)
  done

  echo "$RESPONSE" | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 2: The agentic loop.
  # Uses jq for cross-turn message-array state — building an agentic loop in shell
  # requires JSON manipulation beyond ant's single-call --transform scope.
  set -euo pipefail

  run_tool() {
    local name="$1" input="$2"
    if [ "$name" = "create_calendar_event" ]; then
      jq -n --arg title "$(jq -r '.title' <<<"$input")" \
        '{event_id: "evt_123", status: "created", title: $title}'
    else
      printf '{"error": "Unknown tool: %s"}' "$name"
    fi
  }

  # Keep the full conversation history in a JSON array so each turn sees
  # prior context.
  MESSAGES='[{"role": "user", "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."}]'

  call_api() {
    # ant reads the request body as YAML on stdin: no auth headers, no
    # hand-built JSON envelope. The static keys (model, tools, tool_choice)
    # live in a quoted heredoc; the growing messages array is appended as
    # JSON, which YAML accepts as flow syntax.
    {
      cat <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tool_choice: {type: auto, disable_parallel_tool_use: true}
  tools:
    - name: create_calendar_event
      description: Create a calendar event with attendees and optional recurrence.
      input_schema:
        type: object
        properties:
          title: {type: string}
          start: {type: string, format: date-time}
          end: {type: string, format: date-time}
          attendees:
            type: array
            items: {type: string, format: email}
          recurrence:
            type: object
            properties:
              frequency: {enum: [daily, weekly, monthly]}
              count: {type: integer, minimum: 1}
        required: [title, start, end]
  YAML
      printf 'messages: %s\n' "$MESSAGES"
    } | ant messages create --format json
  }

  RESPONSE=$(call_api)

  # Loop until Claude stops asking for tools. Each iteration runs the
  # requested tool, appends the result to history, and asks Claude to
  # continue.
  while [ "$(jq -r '.stop_reason' <<<"$RESPONSE")" = "tool_use" ]; do
    TOOL_USE=$(jq '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")
    TOOL_NAME=$(jq -r '.name' <<<"$TOOL_USE")
    TOOL_INPUT=$(jq -c '.input' <<<"$TOOL_USE")
    TOOL_USE_ID=$(jq -r '.id' <<<"$TOOL_USE")
    RESULT=$(run_tool "$TOOL_NAME" "$TOOL_INPUT")

    MESSAGES=$(jq \
      --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
      --arg tool_use_id "$TOOL_USE_ID" \
      --arg result "$RESULT" \
      '. + [
        {role: "assistant", content: $assistant},
        {role: "user", content: [
          {type: "tool_result", tool_use_id: $tool_use_id, content: $result}
        ]}
      ]' <<<"$MESSAGES")

    RESPONSE=$(call_api)
  done

  jq -r '.content[] | select(.type == "text") | .text' <<<"$RESPONSE"
  ```

  ```python Python
  # Ring 2: The agentic loop.

  import json

  import anthropic

  client = anthropic.Anthropic()

  tools = [
      {
          "name": "create_calendar_event",
          "description": "Create a calendar event with attendees and optional recurrence.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "title": {"type": "string"},
                  "start": {"type": "string", "format": "date-time"},
                  "end": {"type": "string", "format": "date-time"},
                  "attendees": {
                      "type": "array",
                      "items": {"type": "string", "format": "email"},
                  },
                  "recurrence": {
                      "type": "object",
                      "properties": {
                          "frequency": {"enum": ["daily", "weekly", "monthly"]},
                          "count": {"type": "integer", "minimum": 1},
                      },
                  },
              },
              "required": ["title", "start", "end"],
          },
      }
  ]


  def run_tool(name, tool_input):
      if name == "create_calendar_event":
          return {"event_id": "evt_123", "status": "created", "title": tool_input["title"]}
      return {"error": f"Unknown tool: {name}"}


  # Keep the full conversation history in a list so each turn sees prior context.
  messages = [
      {
          "role": "user",
          "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
      }
  ]

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "auto", "disable_parallel_tool_use": True},
      messages=messages,
  )

  # Loop until Claude stops asking for tools. Each iteration runs the requested
  # tool, appends the result to history, and asks Claude to continue.
  while response.stop_reason == "tool_use":
      tool_use = next(block for block in response.content if block.type == "tool_use")
      result = run_tool(tool_use.name, tool_use.input)

      messages.append({"role": "assistant", "content": response.content})
      messages.append(
          {
              "role": "user",
              "content": [
                  {
                      "type": "tool_result",
                      "tool_use_id": tool_use.id,
                      "content": json.dumps(result),
                  }
              ],
          }
      )

      response = client.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=tools,
          tool_choice={"type": "auto", "disable_parallel_tool_use": True},
          messages=messages,
      )

  final_text = next(block for block in response.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 2: The agentic loop.

  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const tools: Anthropic.Tool[] = [
    {
      name: "create_calendar_event",
      description:
        "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: { type: "string" },
          start: { type: "string", format: "date-time" },
          end: { type: "string", format: "date-time" },
          attendees: {
            type: "array",
            items: { type: "string", format: "email" },
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: { enum: ["daily", "weekly", "monthly"] },
              count: { type: "integer", minimum: 1 },
            },
          },
        },
        required: ["title", "start", "end"],
      },
    },
  ];

  function runTool(name: string, input: Record<string, unknown>) {
    if (name === "create_calendar_event") {
      return { event_id: "evt_123", status: "created", title: input.title };
    }
    return { error: `Unknown tool: ${name}` };
  }

  // Keep the full conversation history so each turn sees prior context.
  const messages: Anthropic.MessageParam[] = [
    {
      role: "user",
      content:
        "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
    },
  ];

  let response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "auto", disable_parallel_tool_use: true },
    messages,
  });

  // Loop until Claude stops asking for tools. Each iteration runs the requested
  // tool, appends the result to history, and asks Claude to continue.
  while (response.stop_reason === "tool_use") {
    const toolUse = response.content.find(
      (block): block is Anthropic.ToolUseBlock => block.type === "tool_use",
    )!;
    const result = runTool(toolUse.name, toolUse.input as Record<string, unknown>);

    messages.push({ role: "assistant", content: response.content });
    messages.push({
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: toolUse.id,
          content: JSON.stringify(result),
        },
      ],
    });

    response = await client.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools,
      tool_choice: { type: "auto", disable_parallel_tool_use: true },
      messages,
    });
  }

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  // Ring 2: The agentic loop.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
  ];

  // Run the requested tool and return its result as a string.
  string RunTool(ToolUseBlock toolUse)
  {
      if (toolUse.Name == "create_calendar_event")
      {
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title });
      }
      return JsonSerializer.Serialize(new { error = $"Unknown tool: {toolUse.Name}" });
  }

  var toolChoice = new ToolChoice(new ToolChoiceAuto { DisableParallelToolUse = true });

  // Keep the full conversation history in a list so each turn sees prior context.
  List<MessageParam> messages =
  [
      new()
      {
          Role = Role.User,
          Content = "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
      },
  ];

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = toolChoice,
      Messages = messages,
  });

  // Loop until Claude stops asking for tools. Each iteration runs the requested
  // tool, appends the result to history, and asks Claude to continue.
  while (response.StopReason == StopReason.ToolUse)
  {
      ToolUseBlock? toolUse = null;
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var picked))
          {
              toolUse = picked;
              break;
          }
      }
      var result = RunTool(toolUse!);

      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
      });
      messages.Add(new()
      {
          Role = Role.User,
          Content = new MessageParamContent(
          [
              new ContentBlockParam(new ToolResultBlockParam() { ToolUseID = toolUse!.ID, Content = result }),
          ]),
      });

      response = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Tools = tools,
          ToolChoice = toolChoice,
          Messages = messages,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 2: The agentic loop.

  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func runTool(name string, input map[string]any) string {
  	if name == "create_calendar_event" {
  		title, _ := input["title"].(string)
  		return fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, title)
  	}
  	return fmt.Sprintf(`{"error": "Unknown tool: %s"}`, name)
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  	}

  	toolChoice := anthropic.ToolChoiceUnionParam{
  		OfAuto: &anthropic.ToolChoiceAutoParam{DisableParallelToolUse: anthropic.Bool(true)},
  	}

  	// Keep the full conversation history in a slice so each turn sees prior context.
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			"Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.",
  		)),
  	}

  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus5_5,
  		MaxTokens:  1024,
  		Tools:      tools,
  		ToolChoice: toolChoice,
  		Messages:   messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Loop until Claude stops asking for tools. Each iteration runs the requested
  	// tool, appends the result to history, and asks Claude to continue.
  	for response.StopReason == "tool_use" {
  		var toolUse anthropic.ContentBlockUnion
  		for _, block := range response.Content {
  			if block.Type == "tool_use" {
  				toolUse = block
  				break
  			}
  		}

  		var input map[string]any
  		if err := json.Unmarshal(toolUse.Input, &input); err != nil {
  			log.Fatal(err)
  		}
  		result := runTool(toolUse.Name, input)

  		var assistantContent []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			assistantContent = append(assistantContent, block.ToParam())
  		}
  		messages = append(messages, anthropic.NewAssistantMessage(assistantContent...))
  		messages = append(messages, anthropic.NewUserMessage(
  			anthropic.NewToolResultBlock(toolUse.ID, result, false),
  		))

  		response, err = client.Messages.New(ctx, anthropic.MessageNewParams{
  			Model:      anthropic.ModelClaudeOpus5_5,
  			MaxTokens:  1024,
  			Tools:      tools,
  			ToolChoice: toolChoice,
  			Messages:   messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  	}

  	for _, block := range response.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 2: The agentic loop.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolChoiceAuto;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.ArrayList;
  import java.util.List;
  import java.util.Map;

  String runTool(ToolUseBlock toolUse) {
      // The raw tool input is a JSON object; read fields out of it as a map.
      Map<String, JsonValue> input = (Map<String, JsonValue>) toolUse._input().asObject().get();
      if (toolUse.name().equals("create_calendar_event")) {
          String title = input.containsKey("title") ? input.get("title").asStringOrThrow() : "";
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
      return "{\"error\": \"Unknown tool: " + toolUse.name() + "\"}";
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      ToolChoiceAuto toolChoice = ToolChoiceAuto.builder()
          .disableParallelToolUse(true)
          .build();

      // Keep the full conversation history in a list so each turn sees prior context.
      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.")
          .build());

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .toolChoice(toolChoice)
          .messages(messages)
          .build());

      // Loop until Claude stops asking for tools. Each iteration runs the requested
      // tool, appends the result to history, and asks Claude to continue.
      while (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.TOOL_USE)) {
          ToolUseBlock toolUse = response.content().stream()
              .flatMap(block -> block.toolUse().stream())
              .findFirst()
              .orElseThrow();
          String result = runTool(toolUse);

          messages.add(response.toParam());
          messages.add(MessageParam.builder()
              .role(MessageParam.Role.USER)
              .contentOfBlockParams(List.of(ContentBlockParam.ofToolResult(
                  ToolResultBlockParam.builder()
                      .toolUseId(toolUse.id())
                      .content(result)
                      .build())))
              .build());

          response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .addTool(calendarTool)
              .toolChoice(toolChoice)
              .messages(messages)
              .build());
      }

      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 2: The agentic loop.

  use Anthropic\Client;
  use Anthropic\Messages\ToolChoiceAuto;

  $client = new Client();

  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
  ];

  function runTool(string $name, array $input): string
  {
      if ($name === 'create_calendar_event') {
          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      }

      return json_encode(['error' => "Unknown tool: {$name}"]);
  }

  $toolChoice = ToolChoiceAuto::with(disableParallelToolUse: true);

  // Keep the full conversation history in an array so each turn sees prior context.
  $messages = [
      [
          'role' => 'user',
          'content' => 'Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com.',
      ],
  ];

  $response = $client->messages->create(
      model: 'claude-opus-5-5',
      maxTokens: 1024,
      tools: $tools,
      toolChoice: $toolChoice,
      messages: $messages,
  );

  // Loop until Claude stops asking for tools. Each iteration runs the requested
  // tool, appends the result to history, and asks Claude to continue.
  while ($response->stopReason === 'tool_use') {
      $toolUse = null;
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $toolUse = $block;
              break;
          }
      }

      $result = runTool($toolUse->name, $toolUse->input);

      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = [
          'role' => 'user',
          'content' => [
              [
                  'type' => 'tool_result',
                  'tool_use_id' => $toolUse->id,
                  'content' => $result,
              ],
          ],
      ];

      $response = $client->messages->create(
          model: 'claude-opus-5-5',
          maxTokens: 1024,
          tools: $tools,
          toolChoice: $toolChoice,
          messages: $messages,
      );
  }

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 2: The agentic loop.

  require "anthropic"

  client = Anthropic::Client.new

  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    }
  ]

  def run_tool(name, input)
    case name
    when "create_calendar_event"
      JSON.generate({event_id: "evt_123", status: "created", title: input[:title]})
    else
      JSON.generate({error: "Unknown tool: #{name}"})
    end
  end

  tool_choice = {type: "auto", disable_parallel_tool_use: true}

  # Keep the full conversation history in an array so each turn sees prior context.
  messages = [
    {
      role: "user",
      content: "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."
    }
  ]

  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: tools,
    tool_choice: tool_choice,
    messages: messages
  )

  # Loop until Claude stops asking for tools. Each iteration runs the requested
  # tool, appends the result to history, and asks Claude to continue.
  while response.stop_reason == :tool_use
    tool_use = response.content.find { |block| block.type == :tool_use }
    result = run_tool(tool_use.name, tool_use.input)

    messages << {role: "assistant", content: response.content}
    messages << {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: result
        }
      ]
    }

    response = client.messages.create(
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: tools,
      tool_choice: tool_choice,
      messages: messages
    )
  end

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**What to expect**

```text Output wrap
I've set up your weekly team standup for the next 4 Mondays at 9am with Alice, Bob, and Carol invited.
```

The loop might run once or several times depending on how Claude breaks down the task. Your code no longer needs to know in advance.

## Ring 3: Multiple tools, parallel calls

Agents rarely have just one capability. Add a second tool, `list_calendar_events`, so Claude can check the existing schedule before creating something new.

When Claude has multiple independent tool calls to make, it might return several `tool_use` blocks in a single response. Your loop needs to process all of them and send back all results together in one user message. Iterate over every `tool_use` block in `response.content`, not just the first.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 3: Multiple tools, parallel calls.

  TOOLS='[
    {
      "name": "create_calendar_event",
      "description": "Create a calendar event with attendees and optional recurrence.",
      "input_schema": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "start": {"type": "string", "format": "date-time"},
          "end": {"type": "string", "format": "date-time"},
          "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
          "recurrence": {
            "type": "object",
            "properties": {
              "frequency": {"enum": ["daily", "weekly", "monthly"]},
              "count": {"type": "integer", "minimum": 1}
            }
          }
        },
        "required": ["title", "start", "end"]
      }
    },
    {
      "name": "list_calendar_events",
      "description": "List all calendar events on a given date.",
      "input_schema": {
        "type": "object",
        "properties": {"date": {"type": "string", "format": "date"}},
        "required": ["date"]
      }
    }
  ]'

  run_tool() {
    case "$1" in
      create_calendar_event)
        jq -n --arg title "$(echo "$2" | jq -r '.title')" '{event_id: "evt_123", status: "created", title: $title}' ;;
      list_calendar_events)
        echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
      *)
        echo "{\"error\": \"Unknown tool: $1\"}" ;;
    esac
  }

  MESSAGES='[{"role": "user", "content": "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts."}]'

  call_api() {
    curl -s https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d "$(jq -n --argjson tools "$TOOLS" --argjson messages "$MESSAGES" \
        '{model: "claude-opus-5-5", max_tokens: 1024, tools: $tools, messages: $messages}')"
  }

  RESPONSE=$(call_api)

  while [ "$(echo "$RESPONSE" | jq -r '.stop_reason')" = "tool_use" ]; do
    # A single response can contain multiple tool_use blocks. Process all of
    # them and return all results together in one user message.
    TOOL_RESULTS='[]'
    while read -r block; do
      NAME=$(echo "$block" | jq -r '.name')
      INPUT=$(echo "$block" | jq -c '.input')
      ID=$(echo "$block" | jq -r '.id')
      RESULT=$(run_tool "$NAME" "$INPUT")
      TOOL_RESULTS=$(echo "$TOOL_RESULTS" | jq --arg id "$ID" --arg result "$RESULT" \
        '. + [{type: "tool_result", tool_use_id: $id, content: $result}]')
    done < <(echo "$RESPONSE" | jq -c '.content[] | select(.type == "tool_use")')

    MESSAGES=$(echo "$MESSAGES" | jq \
      --argjson assistant "$(echo "$RESPONSE" | jq '.content')" \
      --argjson results "$TOOL_RESULTS" \
      '. + [{role: "assistant", content: $assistant}, {role: "user", content: $results}]')

    RESPONSE=$(call_api)
  done

  echo "$RESPONSE" | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 3: Multiple tools, parallel calls.
  # Uses jq for cross-turn message-array state — building an agentic loop in shell
  # requires JSON manipulation beyond ant's single-call --transform scope.
  set -euo pipefail

  run_tool() {
    case "$1" in
      create_calendar_event)
        jq -n --arg title "$(jq -r '.title' <<<"$2")" \
          '{event_id: "evt_123", status: "created", title: $title}' ;;
      list_calendar_events)
        echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
      *)
        printf '{"error": "Unknown tool: %s"}' "$1" ;;
    esac
  }

  MESSAGES='[{"role": "user", "content": "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts."}]'

  call_api() {
    # ant reads the request body as YAML on stdin: no auth headers, no
    # hand-built JSON envelope. The static keys (model, tools) live in a
    # quoted heredoc; the growing messages array is appended as JSON,
    # which YAML accepts as flow syntax.
    {
      cat <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tools:
    - name: create_calendar_event
      description: Create a calendar event with attendees and optional recurrence.
      input_schema:
        type: object
        properties:
          title: {type: string}
          start: {type: string, format: date-time}
          end: {type: string, format: date-time}
          attendees:
            type: array
            items: {type: string, format: email}
          recurrence:
            type: object
            properties:
              frequency: {enum: [daily, weekly, monthly]}
              count: {type: integer, minimum: 1}
        required: [title, start, end]
    - name: list_calendar_events
      description: List all calendar events on a given date.
      input_schema:
        type: object
        properties:
          date: {type: string, format: date}
        required: [date]
  YAML
      printf 'messages: %s\n' "$MESSAGES"
    } | ant messages create --format json
  }

  RESPONSE=$(call_api)

  while [ "$(jq -r '.stop_reason' <<<"$RESPONSE")" = "tool_use" ]; do
    # A single response can contain multiple tool_use blocks. Process all
    # of them and return all results together in one user message.
    TOOL_RESULTS='[]'
    while read -r block; do
      NAME=$(jq -r '.name' <<<"$block")
      INPUT=$(jq -c '.input' <<<"$block")
      ID=$(jq -r '.id' <<<"$block")
      RESULT=$(run_tool "$NAME" "$INPUT")
      TOOL_RESULTS=$(jq --arg id "$ID" --arg result "$RESULT" \
        '. + [{type: "tool_result", tool_use_id: $id, content: $result}]' \
        <<<"$TOOL_RESULTS")
    done < <(jq -c '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")

    MESSAGES=$(jq \
      --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
      --argjson results "$TOOL_RESULTS" \
      '. + [
        {role: "assistant", content: $assistant},
        {role: "user", content: $results}
      ]' <<<"$MESSAGES")

    RESPONSE=$(call_api)
  done

  jq -r '.content[] | select(.type == "text") | .text' <<<"$RESPONSE"
  ```

  ```python Python
  # Ring 3: Multiple tools, parallel calls.

  import json

  import anthropic

  client = anthropic.Anthropic()

  tools = [
      {
          "name": "create_calendar_event",
          "description": "Create a calendar event with attendees and optional recurrence.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "title": {"type": "string"},
                  "start": {"type": "string", "format": "date-time"},
                  "end": {"type": "string", "format": "date-time"},
                  "attendees": {
                      "type": "array",
                      "items": {"type": "string", "format": "email"},
                  },
                  "recurrence": {
                      "type": "object",
                      "properties": {
                          "frequency": {"enum": ["daily", "weekly", "monthly"]},
                          "count": {"type": "integer", "minimum": 1},
                      },
                  },
              },
              "required": ["title", "start", "end"],
          },
      },
      {
          "name": "list_calendar_events",
          "description": "List all calendar events on a given date.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "date": {"type": "string", "format": "date"},
              },
              "required": ["date"],
          },
      },
  ]


  def run_tool(name, tool_input):
      if name == "create_calendar_event":
          return {"event_id": "evt_123", "status": "created", "title": tool_input["title"]}
      if name == "list_calendar_events":
          return {"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}
      return {"error": f"Unknown tool: {name}"}


  messages = [
      {
          "role": "user",
          "content": "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
      }
  ]

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=tools,
      messages=messages,
  )

  while response.stop_reason == "tool_use":
      # A single response can contain multiple tool_use blocks. Process all of
      # them and return all results together in one user message.
      tool_results = []
      for block in response.content:
          if block.type == "tool_use":
              result = run_tool(block.name, block.input)
              tool_results.append(
                  {
                      "type": "tool_result",
                      "tool_use_id": block.id,
                      "content": json.dumps(result),
                  }
              )

      messages.append({"role": "assistant", "content": response.content})
      messages.append({"role": "user", "content": tool_results})

      response = client.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=tools,
          messages=messages,
      )

  final_text = next(block for block in response.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 3: Multiple tools, parallel calls.

  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const tools: Anthropic.Tool[] = [
    {
      name: "create_calendar_event",
      description:
        "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: { type: "string" },
          start: { type: "string", format: "date-time" },
          end: { type: "string", format: "date-time" },
          attendees: {
            type: "array",
            items: { type: "string", format: "email" },
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: { enum: ["daily", "weekly", "monthly"] },
              count: { type: "integer", minimum: 1 },
            },
          },
        },
        required: ["title", "start", "end"],
      },
    },
    {
      name: "list_calendar_events",
      description: "List all calendar events on a given date.",
      input_schema: {
        type: "object",
        properties: {
          date: { type: "string", format: "date" },
        },
        required: ["date"],
      },
    },
  ];

  function runTool(name: string, input: Record<string, unknown>) {
    if (name === "create_calendar_event") {
      return { event_id: "evt_123", status: "created", title: input.title };
    }
    if (name === "list_calendar_events") {
      return {
        events: [{ title: "Existing meeting", start: "14:00", end: "15:00" }],
      };
    }
    return { error: `Unknown tool: ${name}` };
  }

  const messages: Anthropic.MessageParam[] = [
    {
      role: "user",
      content:
        "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
    },
  ];

  let response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools,
    messages,
  });

  while (response.stop_reason === "tool_use") {
    // A single response can contain multiple tool_use blocks. Process all of
    // them and return all results together in one user message.
    const toolResults: Anthropic.ToolResultBlockParam[] = [];
    for (const block of response.content) {
      if (block.type === "tool_use") {
        const result = runTool(block.name, block.input as Record<string, unknown>);
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: JSON.stringify(result),
        });
      }
    }

    messages.push({ role: "assistant", content: response.content });
    messages.push({ role: "user", content: toolResults });

    response = await client.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools,
      messages,
    });
  }

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  // Ring 3: Multiple tools, parallel calls.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
      new ToolUnion(new Tool()
      {
          Name = "list_calendar_events",
          Description = "List all calendar events on a given date.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["date"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date" }),
              },
              Required = ["date"],
          },
      }),
  ];

  string RunTool(ToolUseBlock toolUse)
  {
      if (toolUse.Name == "create_calendar_event")
      {
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title });
      }
      if (toolUse.Name == "list_calendar_events")
      {
          return """{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}""";
      }
      return JsonSerializer.Serialize(new { error = $"Unknown tool: {toolUse.Name}" });
  }

  List<MessageParam> messages =
  [
      new()
      {
          Role = Role.User,
          Content = "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
      },
  ];

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Tools = tools,
      Messages = messages,
  });

  while (response.StopReason == StopReason.ToolUse)
  {
      // A single response can contain multiple tool_use blocks. Process all of
      // them and return all results together in one user message.
      List<ContentBlockParam> toolResults = [];
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              toolResults.Add(new ContentBlockParam(new ToolResultBlockParam()
              {
                  ToolUseID = toolUse.ID,
                  Content = RunTool(toolUse),
              }));
          }
      }

      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
      });
      messages.Add(new() { Role = Role.User, Content = new MessageParamContent(toolResults) });

      response = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Tools = tools,
          Messages = messages,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 3: Multiple tools, parallel calls.

  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func runTool(name string, input map[string]any) string {
  	if name == "create_calendar_event" {
  		title, _ := input["title"].(string)
  		return fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, title)
  	}
  	if name == "list_calendar_events" {
  		return `{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}`
  	}
  	return fmt.Sprintf(`{"error": "Unknown tool: %s"}`, name)
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "list_calendar_events",
  			Description: anthropic.String("List all calendar events on a given date."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"date": map[string]any{"type": "string", "format": "date"},
  				},
  				Required: []string{"date"},
  			},
  		}},
  	}

  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			"Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
  		)),
  	}

  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 1024,
  		Tools:     tools,
  		Messages:  messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for response.StopReason == "tool_use" {
  		// A single response can contain multiple tool_use blocks. Process all of
  		// them and return all results together in one user message.
  		var toolResults []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			if block.Type == "tool_use" {
  				var input map[string]any
  				if err := json.Unmarshal(block.Input, &input); err != nil {
  					log.Fatal(err)
  				}
  				result := runTool(block.Name, input)
  				toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, result, false))
  			}
  		}

  		var assistantContent []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			assistantContent = append(assistantContent, block.ToParam())
  		}
  		messages = append(messages, anthropic.NewAssistantMessage(assistantContent...))
  		messages = append(messages, anthropic.NewUserMessage(toolResults...))

  		response, err = client.Messages.New(ctx, anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5_5,
  			MaxTokens: 1024,
  			Tools:     tools,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  	}

  	for _, block := range response.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 3: Multiple tools, parallel calls.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.ArrayList;
  import java.util.List;
  import java.util.Map;

  String runTool(ToolUseBlock toolUse) {
      // The raw tool input is a JSON object; read fields out of it as a map.
      Map<String, JsonValue> input = (Map<String, JsonValue>) toolUse._input().asObject().get();
      if (toolUse.name().equals("create_calendar_event")) {
          String title = input.containsKey("title") ? input.get("title").asStringOrThrow() : "";
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
      if (toolUse.name().equals("list_calendar_events")) {
          return "{\"events\": [{\"title\": \"Existing meeting\", \"start\": \"14:00\", \"end\": \"15:00\"}]}";
      }
      return "{\"error\": \"Unknown tool: " + toolUse.name() + "\"}";
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      Tool listTool = Tool.builder()
          .name("list_calendar_events")
          .description("List all calendar events on a given date.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "date", Map.of("type", "string", "format", "date")
              )))
              .required(List.of("date"))
              .build())
          .build();

      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.")
          .build());

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .addTool(listTool)
          .messages(messages)
          .build());

      while (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.TOOL_USE)) {
          // A single response can contain multiple tool_use blocks. Process all of
          // them and return all results together in one user message.
          List<ContentBlockParam> toolResults = new ArrayList<>();
          for (ContentBlock block : response.content()) {
              if (block.toolUse().isPresent()) {
                  ToolUseBlock toolUse = block.toolUse().get();
                  toolResults.add(ContentBlockParam.ofToolResult(
                      ToolResultBlockParam.builder()
                          .toolUseId(toolUse.id())
                          .content(runTool(toolUse))
                          .build()));
              }
          }

          messages.add(response.toParam());
          messages.add(MessageParam.builder()
              .role(MessageParam.Role.USER)
              .contentOfBlockParams(toolResults)
              .build());

          response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .addTool(calendarTool)
              .addTool(listTool)
              .messages(messages)
              .build());
      }

      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 3: Multiple tools, parallel calls.

  use Anthropic\Client;

  $client = new Client();

  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
      [
          'name' => 'list_calendar_events',
          'description' => 'List all calendar events on a given date.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'date' => ['type' => 'string', 'format' => 'date'],
              ],
              'required' => ['date'],
          ],
      ],
  ];

  function runTool(string $name, array $input): string
  {
      if ($name === 'create_calendar_event') {
          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      }
      if ($name === 'list_calendar_events') {
          return json_encode([
              'events' => [['title' => 'Existing meeting', 'start' => '14:00', 'end' => '15:00']],
          ]);
      }

      return json_encode(['error' => "Unknown tool: {$name}"]);
  }

  $messages = [
      [
          'role' => 'user',
          'content' => 'Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.',
      ],
  ];

  $response = $client->messages->create(
      model: 'claude-opus-5-5',
      maxTokens: 1024,
      tools: $tools,
      messages: $messages,
  );

  while ($response->stopReason === 'tool_use') {
      // A single response can contain multiple tool_use blocks. Process all of
      // them and return all results together in one user message.
      $toolResults = [];
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $toolResults[] = [
                  'type' => 'tool_result',
                  'tool_use_id' => $block->id,
                  'content' => runTool($block->name, $block->input),
              ];
          }
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = ['role' => 'user', 'content' => $toolResults];

      $response = $client->messages->create(
          model: 'claude-opus-5-5',
          maxTokens: 1024,
          tools: $tools,
          messages: $messages,
      );
  }

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 3: Multiple tools, parallel calls.

  require "anthropic"

  client = Anthropic::Client.new

  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    },
    {
      name: "list_calendar_events",
      description: "List all calendar events on a given date.",
      input_schema: {
        type: "object",
        properties: {
          date: {type: "string", format: "date"}
        },
        required: ["date"]
      }
    }
  ]

  def run_tool(name, input)
    case name
    when "create_calendar_event"
      JSON.generate({event_id: "evt_123", status: "created", title: input[:title]})
    when "list_calendar_events"
      JSON.generate({events: [{title: "Existing meeting", start: "14:00", end: "15:00"}]})
    else
      JSON.generate({error: "Unknown tool: #{name}"})
    end
  end

  messages = [
    {
      role: "user",
      content: "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts."
    }
  ]

  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: tools,
    messages: messages
  )

  while response.stop_reason == :tool_use
    # A single response can contain multiple tool_use blocks. Process all of
    # them and return all results together in one user message.
    tool_results = response.content.select { |block| block.type == :tool_use }.map do |tool_use|
      {
        type: "tool_result",
        tool_use_id: tool_use.id,
        content: run_tool(tool_use.name, tool_use.input)
      }
    end

    messages << {role: "assistant", content: response.content}
    messages << {role: "user", content: tool_results}

    response = client.messages.create(
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: tools,
      messages: messages
    )
  end

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**What to expect**

```text Output wrap
I checked your calendar for Monday, March 30 and found an existing meeting from 2pm to 3pm. I've scheduled the planning session for 10am to 11am to avoid the conflict.
```

For more on concurrent execution and ordering guarantees, see [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use).

## Ring 4: Error handling

Tools fail. A calendar API might reject an event with too many attendees, or a date might be malformed. When a tool raises an error, send the error message back with `is_error: true` instead of crashing. Claude reads the error and can retry with corrected input, ask the user for clarification, or explain the limitation.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 4: Error handling.

  TOOLS='[
    {
      "name": "create_calendar_event",
      "description": "Create a calendar event with attendees and optional recurrence.",
      "input_schema": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "start": {"type": "string", "format": "date-time"},
          "end": {"type": "string", "format": "date-time"},
          "attendees": {"type": "array", "items": {"type": "string", "format": "email"}},
          "recurrence": {
            "type": "object",
            "properties": {
              "frequency": {"enum": ["daily", "weekly", "monthly"]},
              "count": {"type": "integer", "minimum": 1}
            }
          }
        },
        "required": ["title", "start", "end"]
      }
    },
    {
      "name": "list_calendar_events",
      "description": "List all calendar events on a given date.",
      "input_schema": {
        "type": "object",
        "properties": {"date": {"type": "string", "format": "date"}},
        "required": ["date"]
      }
    }
  ]'

  run_tool() {
    case "$1" in
      create_calendar_event)
        local count=$(echo "$2" | jq '.attendees | length // 0')
        if [ "$count" -gt 10 ]; then
          echo "ERROR: Too many attendees (max 10)"
          return 1
        fi
        jq -n --arg title "$(echo "$2" | jq -r '.title')" '{event_id: "evt_123", status: "created", title: $title}' ;;
      list_calendar_events)
        echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
      *)
        echo "ERROR: Unknown tool: $1"
        return 1 ;;
    esac
  }

  EMAILS=$(seq 0 14 | sed 's/.*/user&@example.com/' | paste -sd, -)
  MESSAGES="[{\"role\": \"user\", \"content\": \"Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: $EMAILS\"}]"

  call_api() {
    curl -s https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d "$(jq -n --argjson tools "$TOOLS" --argjson messages "$MESSAGES" \
        '{model: "claude-opus-5-5", max_tokens: 1024, tools: $tools, messages: $messages}')"
  }

  RESPONSE=$(call_api)

  while [ "$(echo "$RESPONSE" | jq -r '.stop_reason')" = "tool_use" ]; do
    TOOL_RESULTS='[]'
    while read -r block; do
      NAME=$(echo "$block" | jq -r '.name')
      INPUT=$(echo "$block" | jq -c '.input')
      ID=$(echo "$block" | jq -r '.id')
      if OUTPUT=$(run_tool "$NAME" "$INPUT"); then
        TOOL_RESULTS=$(echo "$TOOL_RESULTS" | jq --arg id "$ID" --arg result "$OUTPUT" \
          '. + [{type: "tool_result", tool_use_id: $id, content: $result}]')
      else
        # Signal failure so Claude can retry or ask for clarification.
        TOOL_RESULTS=$(echo "$TOOL_RESULTS" | jq --arg id "$ID" --arg result "$OUTPUT" \
          '. + [{type: "tool_result", tool_use_id: $id, content: $result, is_error: true}]')
      fi
    done < <(echo "$RESPONSE" | jq -c '.content[] | select(.type == "tool_use")')

    MESSAGES=$(echo "$MESSAGES" | jq \
      --argjson assistant "$(echo "$RESPONSE" | jq '.content')" \
      --argjson results "$TOOL_RESULTS" \
      '. + [{role: "assistant", content: $assistant}, {role: "user", content: $results}]')

    RESPONSE=$(call_api)
  done

  echo "$RESPONSE" | jq -r '.content[] | select(.type == "text") | .text'
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 4: Error handling.
  # Uses jq for cross-turn message-array state — building an agentic loop in shell
  # requires JSON manipulation beyond ant's single-call --transform scope.
  set -euo pipefail

  run_tool() {
    case "$1" in
      create_calendar_event)
        local count
        count=$(jq '.attendees | length // 0' <<<"$2")
        if [ "$count" -gt 10 ]; then
          echo "ERROR: Too many attendees (max 10)"
          return 1
        fi
        jq -n --arg title "$(jq -r '.title' <<<"$2")" \
          '{event_id: "evt_123", status: "created", title: $title}' ;;
      list_calendar_events)
        echo '{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}' ;;
      *)
        echo "ERROR: Unknown tool: $1"
        return 1 ;;
    esac
  }

  EMAILS=$(seq 0 14 | sed 's/.*/user&@example.com/' | paste -sd, -)
  MESSAGES=$(jq -n --arg msg "Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: $EMAILS" \
    '[{role: "user", content: $msg}]')

  call_api() {
    # ant reads the request body as YAML on stdin: no auth headers, no
    # hand-built JSON envelope. The static keys (model, tools) live in a
    # quoted heredoc; the growing messages array is appended as JSON,
    # which YAML accepts as flow syntax.
    {
      cat <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  tools:
    - name: create_calendar_event
      description: Create a calendar event with attendees and optional recurrence.
      input_schema:
        type: object
        properties:
          title: {type: string}
          start: {type: string, format: date-time}
          end: {type: string, format: date-time}
          attendees:
            type: array
            items: {type: string, format: email}
          recurrence:
            type: object
            properties:
              frequency: {enum: [daily, weekly, monthly]}
              count: {type: integer, minimum: 1}
        required: [title, start, end]
    - name: list_calendar_events
      description: List all calendar events on a given date.
      input_schema:
        type: object
        properties:
          date: {type: string, format: date}
        required: [date]
  YAML
      printf 'messages: %s\n' "$MESSAGES"
    } | ant messages create --format json
  }

  RESPONSE=$(call_api)

  while [ "$(jq -r '.stop_reason' <<<"$RESPONSE")" = "tool_use" ]; do
    TOOL_RESULTS='[]'
    while read -r block; do
      NAME=$(jq -r '.name' <<<"$block")
      INPUT=$(jq -c '.input' <<<"$block")
      ID=$(jq -r '.id' <<<"$block")
      if OUTPUT=$(run_tool "$NAME" "$INPUT"); then
        TOOL_RESULTS=$(jq --arg id "$ID" --arg result "$OUTPUT" \
          '. + [{type: "tool_result", tool_use_id: $id, content: $result}]' \
          <<<"$TOOL_RESULTS")
      else
        # Signal failure so Claude can retry or ask for clarification.
        TOOL_RESULTS=$(jq --arg id "$ID" --arg result "$OUTPUT" \
          '. + [{type: "tool_result", tool_use_id: $id, content: $result, is_error: true}]' \
          <<<"$TOOL_RESULTS")
      fi
    done < <(jq -c '.content[] | select(.type == "tool_use")' <<<"$RESPONSE")

    MESSAGES=$(jq \
      --argjson assistant "$(jq '.content' <<<"$RESPONSE")" \
      --argjson results "$TOOL_RESULTS" \
      '. + [
        {role: "assistant", content: $assistant},
        {role: "user", content: $results}
      ]' <<<"$MESSAGES")

    RESPONSE=$(call_api)
  done

  jq -r '.content[] | select(.type == "text") | .text' <<<"$RESPONSE"
  ```

  ```python Python
  # Ring 4: Error handling.

  import json

  import anthropic

  client = anthropic.Anthropic()

  tools = [
      {
          "name": "create_calendar_event",
          "description": "Create a calendar event with attendees and optional recurrence.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "title": {"type": "string"},
                  "start": {"type": "string", "format": "date-time"},
                  "end": {"type": "string", "format": "date-time"},
                  "attendees": {
                      "type": "array",
                      "items": {"type": "string", "format": "email"},
                  },
                  "recurrence": {
                      "type": "object",
                      "properties": {
                          "frequency": {"enum": ["daily", "weekly", "monthly"]},
                          "count": {"type": "integer", "minimum": 1},
                      },
                  },
              },
              "required": ["title", "start", "end"],
          },
      },
      {
          "name": "list_calendar_events",
          "description": "List all calendar events on a given date.",
          "input_schema": {
              "type": "object",
              "properties": {
                  "date": {"type": "string", "format": "date"},
              },
              "required": ["date"],
          },
      },
  ]


  def run_tool(name, tool_input):
      if name == "create_calendar_event":
          if "attendees" in tool_input and len(tool_input["attendees"]) > 10:
              raise ValueError("Too many attendees (max 10)")
          return {"event_id": "evt_123", "status": "created", "title": tool_input["title"]}
      if name == "list_calendar_events":
          return {"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}
      raise ValueError(f"Unknown tool: {name}")


  messages = [
      {
          "role": "user",
          "content": "Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: " + ", ".join(f"user{i}@example.com" for i in range(15)),
      }
  ]

  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=tools,
      messages=messages,
  )

  while response.stop_reason == "tool_use":
      tool_results = []
      for block in response.content:
          if block.type == "tool_use":
              try:
                  result = run_tool(block.name, block.input)
                  tool_results.append(
                      {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)}
                  )
              except Exception as exc:
                  # Signal failure so Claude can retry or ask for clarification.
                  tool_results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": block.id,
                          "content": str(exc),
                          "is_error": True,
                      }
                  )

      messages.append({"role": "assistant", "content": response.content})
      messages.append({"role": "user", "content": tool_results})

      response = client.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=tools,
          messages=messages,
      )

  final_text = next(block for block in response.content if block.type == "text")
  print(final_text.text)
  ```

  ```typescript TypeScript
  // Ring 4: Error handling.

  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const tools: Anthropic.Tool[] = [
    {
      name: "create_calendar_event",
      description:
        "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: { type: "string" },
          start: { type: "string", format: "date-time" },
          end: { type: "string", format: "date-time" },
          attendees: {
            type: "array",
            items: { type: "string", format: "email" },
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: { enum: ["daily", "weekly", "monthly"] },
              count: { type: "integer", minimum: 1 },
            },
          },
        },
        required: ["title", "start", "end"],
      },
    },
    {
      name: "list_calendar_events",
      description: "List all calendar events on a given date.",
      input_schema: {
        type: "object",
        properties: {
          date: { type: "string", format: "date" },
        },
        required: ["date"],
      },
    },
  ];

  function runTool(name: string, input: Record<string, unknown>) {
    if (name === "create_calendar_event") {
      const attendees = input.attendees as string[] | undefined;
      if (attendees && attendees.length > 10) {
        throw new Error("Too many attendees (max 10)");
      }
      return { event_id: "evt_123", status: "created", title: input.title };
    }
    if (name === "list_calendar_events") {
      return {
        events: [{ title: "Existing meeting", start: "14:00", end: "15:00" }],
      };
    }
    throw new Error(`Unknown tool: ${name}`);
  }

  const emails = Array.from({ length: 15 }, (_, i) => `user${i}@example.com`);
  const messages: Anthropic.MessageParam[] = [
    {
      role: "user",
      content: `Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: ${emails.join(", ")}`,
    },
  ];

  let response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools,
    messages,
  });

  while (response.stop_reason === "tool_use") {
    const toolResults: Anthropic.ToolResultBlockParam[] = [];
    for (const block of response.content) {
      if (block.type === "tool_use") {
        try {
          const result = runTool(block.name, block.input as Record<string, unknown>);
          toolResults.push({
            type: "tool_result",
            tool_use_id: block.id,
            content: JSON.stringify(result),
          });
        } catch (err) {
          // Signal failure so Claude can retry or ask for clarification.
          toolResults.push({
            type: "tool_result",
            tool_use_id: block.id,
            content: String(err),
            is_error: true,
          });
        }
      }
    }

    messages.push({ role: "assistant", content: response.content });
    messages.push({ role: "user", content: toolResults });

    response = await client.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools,
      messages,
    });
  }

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  // Ring 4: Error handling.

  using System;
  using System.Collections.Generic;
  using System.Linq;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  List<ToolUnion> tools =
  [
      new ToolUnion(new Tool()
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date-time" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string", format = "email" },
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      }),
      new ToolUnion(new Tool()
      {
          Name = "list_calendar_events",
          Description = "List all calendar events on a given date.",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["date"] = JsonSerializer.SerializeToElement(new { type = "string", format = "date" }),
              },
              Required = ["date"],
          },
      }),
  ];

  string RunTool(ToolUseBlock toolUse)
  {
      if (toolUse.Name == "create_calendar_event")
      {
          if (toolUse.Input.TryGetValue("attendees", out var attendees) && attendees.GetArrayLength() > 10)
          {
              throw new InvalidOperationException("Too many attendees (max 10)");
          }
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title });
      }
      if (toolUse.Name == "list_calendar_events")
      {
          return """{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}""";
      }
      throw new InvalidOperationException($"Unknown tool: {toolUse.Name}");
  }

  // Build a request that exceeds the tool's attendee limit so the error path runs.
  var emails = string.Join(", ", Enumerable.Range(0, 15).Select(i => $"user{i}@example.com"));

  List<MessageParam> messages =
  [
      new() { Role = Role.User, Content = $"Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: {emails}" },
  ];

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Tools = tools,
      Messages = messages,
  });

  while (response.StopReason == StopReason.ToolUse)
  {
      List<ContentBlockParam> toolResults = [];
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              ToolResultBlockParam toolResult;
              try
              {
                  toolResult = new ToolResultBlockParam() { ToolUseID = toolUse.ID, Content = RunTool(toolUse) };
              }
              catch (Exception e)
              {
                  // Signal failure so Claude can retry or ask for clarification.
                  toolResult = new ToolResultBlockParam()
                  {
                      ToolUseID = toolUse.ID,
                      Content = e.Message,
                      IsError = true,
                  };
              }
              toolResults.Add(new ContentBlockParam(toolResult));
          }
      }

      messages.Add(new()
      {
          Role = Role.Assistant,
          Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList(),
      });
      messages.Add(new() { Role = Role.User, Content = new MessageParamContent(toolResults) });

      response = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Tools = tools,
          Messages = messages,
      });
  }

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 4: Error handling.

  package main

  import (
  	"context"
  	"encoding/json"
  	"fmt"
  	"log"
  	"strings"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func runTool(name string, input map[string]any) (string, error) {
  	if name == "create_calendar_event" {
  		if attendees, ok := input["attendees"].([]any); ok && len(attendees) > 10 {
  			return "", fmt.Errorf("too many attendees (max 10)")
  		}
  		title, _ := input["title"].(string)
  		return fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, title), nil
  	}
  	if name == "list_calendar_events" {
  		return `{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}`, nil
  	}
  	return "", fmt.Errorf("unknown tool: %s", name)
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	tools := []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "create_calendar_event",
  			Description: anthropic.String("Create a calendar event with attendees and optional recurrence."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"title": map[string]any{"type": "string"},
  					"start": map[string]any{"type": "string", "format": "date-time"},
  					"end":   map[string]any{"type": "string", "format": "date-time"},
  					"attendees": map[string]any{
  						"type":  "array",
  						"items": map[string]any{"type": "string", "format": "email"},
  					},
  					"recurrence": map[string]any{
  						"type": "object",
  						"properties": map[string]any{
  							"frequency": map[string]any{"enum": []string{"daily", "weekly", "monthly"}},
  							"count":     map[string]any{"type": "integer", "minimum": 1},
  						},
  					},
  				},
  				Required: []string{"title", "start", "end"},
  			},
  		}},
  		{OfTool: &anthropic.ToolParam{
  			Name:        "list_calendar_events",
  			Description: anthropic.String("List all calendar events on a given date."),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"date": map[string]any{"type": "string", "format": "date"},
  				},
  				Required: []string{"date"},
  			},
  		}},
  	}

  	// Build a request that exceeds the tool's attendee limit so the error path runs.
  	emails := make([]string, 15)
  	for i := range emails {
  		emails[i] = fmt.Sprintf("user%d@example.com", i)
  	}
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock(
  			"Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: " + strings.Join(emails, ", "),
  		)),
  	}

  	response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 1024,
  		Tools:     tools,
  		Messages:  messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for response.StopReason == "tool_use" {
  		var toolResults []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			if block.Type == "tool_use" {
  				var input map[string]any
  				if err := json.Unmarshal(block.Input, &input); err != nil {
  					log.Fatal(err)
  				}
  				result, toolErr := runTool(block.Name, input)
  				if toolErr != nil {
  					// Signal failure so Claude can retry or ask for clarification.
  					toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, toolErr.Error(), true))
  				} else {
  					toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, result, false))
  				}
  			}
  		}

  		var assistantContent []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			assistantContent = append(assistantContent, block.ToParam())
  		}
  		messages = append(messages, anthropic.NewAssistantMessage(assistantContent...))
  		messages = append(messages, anthropic.NewUserMessage(toolResults...))

  		response, err = client.Messages.New(ctx, anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5_5,
  			MaxTokens: 1024,
  			Tools:     tools,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  	}

  	for _, block := range response.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 4: Error handling.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.StopReason;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.Tool.InputSchema;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlock;
  import java.util.ArrayList;
  import java.util.List;
  import java.util.Map;
  import java.util.stream.Collectors;
  import java.util.stream.IntStream;

  String runTool(ToolUseBlock toolUse) {
      // The raw tool input is a JSON object; read fields out of it as a map.
      Map<String, JsonValue> input = (Map<String, JsonValue>) toolUse._input().asObject().get();
      if (toolUse.name().equals("create_calendar_event")) {
          int attendeeCount = input.containsKey("attendees")
              ? ((List<?>) input.get("attendees").asArray().get()).size()
              : 0;
          if (attendeeCount > 10) {
              throw new IllegalArgumentException("Too many attendees (max 10)");
          }
          String title = input.containsKey("title") ? input.get("title").asStringOrThrow() : "";
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
      if (toolUse.name().equals("list_calendar_events")) {
          return "{\"events\": [{\"title\": \"Existing meeting\", \"start\": \"14:00\", \"end\": \"15:00\"}]}";
      }
      throw new IllegalArgumentException("Unknown tool: " + toolUse.name());
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool calendarTool = Tool.builder()
          .name("create_calendar_event")
          .description("Create a calendar event with attendees and optional recurrence.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "title", Map.of("type", "string"),
                  "start", Map.of("type", "string", "format", "date-time"),
                  "end", Map.of("type", "string", "format", "date-time"),
                  "attendees", Map.of(
                      "type", "array",
                      "items", Map.of("type", "string", "format", "email")
                  ),
                  "recurrence", Map.of(
                      "type", "object",
                      "properties", Map.of(
                          "frequency", Map.of("enum", List.of("daily", "weekly", "monthly")),
                          "count", Map.of("type", "integer", "minimum", 1)
                      )
                  )
              )))
              .required(List.of("title", "start", "end"))
              .build())
          .build();

      Tool listTool = Tool.builder()
          .name("list_calendar_events")
          .description("List all calendar events on a given date.")
          .inputSchema(InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "date", Map.of("type", "string", "format", "date")
              )))
              .required(List.of("date"))
              .build())
          .build();

      // Build a request that exceeds the tool's attendee limit so the error path runs.
      String emails = IntStream.range(0, 15)
          .mapToObj(i -> "user" + i + "@example.com")
          .collect(Collectors.joining(", "));

      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: " + emails)
          .build());

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024L)
          .addTool(calendarTool)
          .addTool(listTool)
          .messages(messages)
          .build());

      while (response.stopReason().isPresent()
              && response.stopReason().get().equals(StopReason.TOOL_USE)) {
          List<ContentBlockParam> toolResults = new ArrayList<>();
          for (ContentBlock block : response.content()) {
              if (block.toolUse().isPresent()) {
                  ToolUseBlock toolUse = block.toolUse().get();
                  ToolResultBlockParam.Builder resultBuilder = ToolResultBlockParam.builder()
                      .toolUseId(toolUse.id());
                  try {
                      resultBuilder.content(runTool(toolUse));
                  } catch (Exception e) {
                      // Signal failure so Claude can retry or ask for clarification.
                      resultBuilder.content(e.getMessage()).isError(true);
                  }
                  toolResults.add(ContentBlockParam.ofToolResult(resultBuilder.build()));
              }
          }

          messages.add(response.toParam());
          messages.add(MessageParam.builder()
              .role(MessageParam.Role.USER)
              .contentOfBlockParams(toolResults)
              .build());

          response = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .addTool(calendarTool)
              .addTool(listTool)
              .messages(messages)
              .build());
      }

      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 4: Error handling.

  use Anthropic\Client;

  $client = new Client();

  $tools = [
      [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string'],
                  'start' => ['type' => 'string', 'format' => 'date-time'],
                  'end' => ['type' => 'string', 'format' => 'date-time'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string', 'format' => 'email'],
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
      [
          'name' => 'list_calendar_events',
          'description' => 'List all calendar events on a given date.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'date' => ['type' => 'string', 'format' => 'date'],
              ],
              'required' => ['date'],
          ],
      ],
  ];

  function runTool(string $name, array $input): string
  {
      if ($name === 'create_calendar_event') {
          if (count($input['attendees'] ?? []) > 10) {
              throw new InvalidArgumentException('Too many attendees (max 10)');
          }

          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      }
      if ($name === 'list_calendar_events') {
          return json_encode([
              'events' => [['title' => 'Existing meeting', 'start' => '14:00', 'end' => '15:00']],
          ]);
      }

      throw new InvalidArgumentException("Unknown tool: {$name}");
  }

  // Build a request that exceeds the tool's attendee limit so the error path runs.
  $emails = array_map(fn (int $i): string => "user{$i}@example.com", range(0, 14));
  $messages = [
      [
          'role' => 'user',
          'content' => 'Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: ' . implode(', ', $emails),
      ],
  ];

  $response = $client->messages->create(
      model: 'claude-opus-5-5',
      maxTokens: 1024,
      tools: $tools,
      messages: $messages,
  );

  while ($response->stopReason === 'tool_use') {
      $toolResults = [];
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              try {
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => runTool($block->name, $block->input),
                  ];
              } catch (Exception $e) {
                  // Signal failure so Claude can retry or ask for clarification.
                  $toolResults[] = [
                      'type' => 'tool_result',
                      'tool_use_id' => $block->id,
                      'content' => $e->getMessage(),
                      'is_error' => true,
                  ];
              }
          }
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = ['role' => 'user', 'content' => $toolResults];

      $response = $client->messages->create(
          model: 'claude-opus-5-5',
          maxTokens: 1024,
          tools: $tools,
          messages: $messages,
      );
  }

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 4: Error handling.

  require "anthropic"

  client = Anthropic::Client.new

  tools = [
    {
      name: "create_calendar_event",
      description: "Create a calendar event with attendees and optional recurrence.",
      input_schema: {
        type: "object",
        properties: {
          title: {type: "string"},
          start: {type: "string", format: "date-time"},
          end: {type: "string", format: "date-time"},
          attendees: {
            type: "array",
            items: {type: "string", format: "email"}
          },
          recurrence: {
            type: "object",
            properties: {
              frequency: {enum: ["daily", "weekly", "monthly"]},
              count: {type: "integer", minimum: 1}
            }
          }
        },
        required: ["title", "start", "end"]
      }
    },
    {
      name: "list_calendar_events",
      description: "List all calendar events on a given date.",
      input_schema: {
        type: "object",
        properties: {
          date: {type: "string", format: "date"}
        },
        required: ["date"]
      }
    }
  ]

  def run_tool(name, input)
    case name
    when "create_calendar_event"
      attendees = input[:attendees]
      raise ArgumentError, "Too many attendees (max 10)" if attendees && attendees.length > 10
      JSON.generate({event_id: "evt_123", status: "created", title: input[:title]})
    when "list_calendar_events"
      JSON.generate({events: [{title: "Existing meeting", start: "14:00", end: "15:00"}]})
    else
      raise ArgumentError, "Unknown tool: #{name}"
    end
  end

  # Build a request that exceeds the tool's attendee limit so the error path runs.
  emails = (0...15).map { |i| "user#{i}@example.com" }
  messages = [
    {
      role: "user",
      content: "Schedule a one-hour all-hands on Monday, March 30, 2026 at 10am with everyone: #{emails.join(", ")}"
    }
  ]

  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: tools,
    messages: messages
  )

  while response.stop_reason == :tool_use
    tool_results = response.content.select { |block| block.type == :tool_use }.map do |tool_use|
      begin
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: run_tool(tool_use.name, tool_use.input)
        }
      rescue => e
        # Signal failure so Claude can retry or ask for clarification.
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: e.message,
          is_error: true
        }
      end
    end

    messages << {role: "assistant", content: response.content}
    messages << {role: "user", content: tool_results}

    response = client.messages.create(
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: tools,
      messages: messages
    )
  end

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**What to expect**

```text Output wrap
I tried to schedule the all-hands but the calendar only allows 10 attendees per event. I can split this into two sessions, or you can let me know which 10 people to prioritize.
```

The `is_error` flag is the only difference from a successful result. Claude sees the flag and the error text, and responds accordingly. See [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) for the full error-handling reference.

## Ring 5: The Tool Runner SDK abstraction

Rings 2 through 4 wrote the same loop by hand: call the API, check `stop_reason`, run tools, append results, repeat. The Tool Runner does this for you. Define each tool as a function, pass the list to `client.beta.messages.tool_runner()` (typescript: `client.beta.messages.toolRunner()`; java: `client.beta().messages().toolRunner()`; php: `$client->beta->messages->toolRunner()`; csharp: `client.Beta.Messages.ToolRunner()`; go: `client.Beta.Messages.NewToolRunner()`), and retrieve the final message once the loop completes. Error wrapping, result formatting, and conversation management are handled internally.

Each SDK provides a helper that turns an ordinary function into a runnable tool and derives the input schema from its signature; the tabs below show the idiomatic form for each language.

<CodeGroup>
  ```bash cURL
  #!/bin/bash
  # Ring 5: The Tool Runner SDK abstraction.

  # The Tool Runner SDK abstraction is available in all seven SDKs: Python,
  # TypeScript, C#, Go, Java, PHP, and Ruby. There is no equivalent for raw
  # curl requests. Switch to any SDK tab to see Ring 5, or keep the Ring 4
  # loop as your shell implementation.
  ```

  ```bash CLI
  #!/usr/bin/env bash
  # Ring 5: The Tool Runner SDK abstraction.
  set -euo pipefail

  # The Tool Runner SDK abstraction is available in all seven SDKs: Python,
  # TypeScript, C#, Go, Java, PHP, and Ruby. The ant CLI exposes the Messages
  # API directly and has no equivalent helper. Switch to any SDK tab to see
  # Ring 5, or keep the Ring 4 loop as your CLI implementation.
  ```

  ```python Python
  # Ring 5: The Tool Runner SDK abstraction.

  import json

  import anthropic
  from anthropic import beta_tool

  client = anthropic.Anthropic()


  @beta_tool
  def create_calendar_event(
      title: str,
      start: str,
      end: str,
      attendees: list[str] | None = None,
      recurrence: dict | None = None,
  ) -> str:
      """Create a calendar event with attendees and optional recurrence.

      Args:
          title: Event title.
          start: Start time in ISO 8601 format.
          end: End time in ISO 8601 format.
          attendees: Email addresses to invite.
          recurrence: Dict with 'frequency' (daily, weekly, monthly) and 'count'.
      """
      if attendees and len(attendees) > 10:
          raise ValueError("Too many attendees (max 10)")
      return json.dumps({"event_id": "evt_123", "status": "created", "title": title})


  @beta_tool
  def list_calendar_events(date: str) -> str:
      """List all calendar events on a given date.

      Args:
          date: Date in YYYY-MM-DD format.
      """
      return json.dumps({"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]})


  final_message = client.beta.messages.tool_runner(
      model="claude-opus-5-5",
      max_tokens=1024,
      tools=[create_calendar_event, list_calendar_events],
      messages=[
          {
              "role": "user",
              "content": "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
          }
      ],
  ).until_done()

  for block in final_message.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  // Ring 5: The Tool Runner SDK abstraction.

  import Anthropic from "@anthropic-ai/sdk";
  import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
  import { z } from "zod";

  const client = new Anthropic();

  const createCalendarEvent = betaZodTool({
    name: "create_calendar_event",
    description:
      "Create a calendar event with attendees and optional recurrence.",
    inputSchema: z.object({
      title: z.string(),
      start: z.string().datetime(),
      end: z.string().datetime(),
      attendees: z.array(z.string().email()).optional(),
      recurrence: z
        .object({
          frequency: z.enum(["daily", "weekly", "monthly"]),
          count: z.number().int().min(1),
        })
        .optional(),
    }),
    run: async (input) => {
      if (input.attendees && input.attendees.length > 10) {
        throw new Error("Too many attendees (max 10)");
      }
      return JSON.stringify({
        event_id: "evt_123",
        status: "created",
        title: input.title,
      });
    },
  });

  const listCalendarEvents = betaZodTool({
    name: "list_calendar_events",
    description: "List all calendar events on a given date.",
    inputSchema: z.object({
      date: z.string().date(),
    }),
    run: async () => {
      return JSON.stringify({
        events: [{ title: "Existing meeting", start: "14:00", end: "15:00" }],
      });
    },
  });

  const finalMessage = await client.beta.messages.toolRunner({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: [createCalendarEvent, listCalendarEvents],
    messages: [
      {
        role: "user",
        content:
          "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
      },
    ],
  });

  for (const block of finalMessage.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  // Ring 5: The Tool Runner SDK abstraction.

  using System;
  using System.Collections.Generic;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Helpers.Beta;
  using Anthropic.Models.Beta.Messages;
  using MessageCreateParams = Anthropic.Models.Beta.Messages.MessageCreateParams;
  using InputSchema = Anthropic.Models.Beta.Messages.InputSchema;
  using Role = Anthropic.Models.Beta.Messages.Role;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  // Define each tool as a runnable tool: the definition carries the JSON Schema
  // and the Run callback holds the implementation. Throwing an exception sends
  // the message back to Claude as a tool result with is_error set.
  var createCalendarEvent = new BetaRunnableTool
  {
      Name = "create_calendar_event",
      Definition = new BetaTool
      {
          Name = "create_calendar_event",
          Description = "Create a calendar event with attendees and optional recurrence.",
          InputSchema = new InputSchema
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["title"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Event title" }),
                  ["start"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Start time in ISO 8601 format" }),
                  ["end"] = JsonSerializer.SerializeToElement(new { type = "string", description = "End time in ISO 8601 format" }),
                  ["attendees"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "array",
                      items = new { type = "string" },
                      description = "Email addresses to invite",
                  }),
                  ["recurrence"] = JsonSerializer.SerializeToElement(new
                  {
                      type = "object",
                      properties = new
                      {
                          frequency = new { @enum = new[] { "daily", "weekly", "monthly" } },
                          count = new { type = "integer", minimum = 1 },
                      },
                  }),
              },
              Required = ["title", "start", "end"],
          },
      },
      Run = (toolUse, _) =>
      {
          if (toolUse.Input.TryGetValue("attendees", out var attendees) && attendees.GetArrayLength() > 10)
          {
              throw new InvalidOperationException("Too many attendees (max 10)");
          }
          var title = toolUse.Input.TryGetValue("title", out var t) ? t.GetString() : "";
          return Task.FromResult<BetaToolResultBlockParamContent>(
              JsonSerializer.Serialize(new { event_id = "evt_123", status = "created", title })
          );
      },
  };

  var listCalendarEvents = new BetaRunnableTool
  {
      Name = "list_calendar_events",
      Definition = new BetaTool
      {
          Name = "list_calendar_events",
          Description = "List all calendar events on a given date.",
          InputSchema = new InputSchema
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["date"] = JsonSerializer.SerializeToElement(new { type = "string", description = "Date in YYYY-MM-DD format" }),
              },
              Required = ["date"],
          },
      },
      Run = (toolUse, _) => Task.FromResult<BetaToolResultBlockParamContent>(
          """{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}"""
      ),
  };

  // The runner calls the API, runs requested tools, and feeds results back
  // until Claude produces a final answer.
  var runner = client.Beta.Messages.ToolRunner(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
              },
          ],
      },
      [createCalendarEvent, listCalendarEvents]
  );

  BetaMessage? finalMessage = null;
  await foreach (var message in runner)
  {
      finalMessage = message;
  }

  foreach (var block in finalMessage!.Content)
  {
      if (block.TryPickText(out var text))
      {
          Console.WriteLine(text.Text);
      }
  }
  ```

  ```go Go
  // Ring 5: The Tool Runner SDK abstraction.

  package main

  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/toolrunner"
  )

  // The input structs define each tool's schema. The tool runner generates the
  // JSON Schema from the struct fields and their jsonschema tags.
  type RecurrenceInput struct {
  	Frequency string `json:"frequency,omitempty" jsonschema:"enum=daily,enum=weekly,enum=monthly,description=How often the event repeats"`
  	Count     int    `json:"count,omitempty" jsonschema:"description=Number of occurrences"`
  }

  type CreateCalendarEventInput struct {
  	Title      string           `json:"title" jsonschema:"required,description=Event title"`
  	Start      string           `json:"start" jsonschema:"required,description=Start time in ISO 8601 format"`
  	End        string           `json:"end" jsonschema:"required,description=End time in ISO 8601 format"`
  	Attendees  []string         `json:"attendees,omitempty" jsonschema:"description=Email addresses to invite"`
  	Recurrence *RecurrenceInput `json:"recurrence,omitempty"`
  }

  type ListCalendarEventsInput struct {
  	Date string `json:"date" jsonschema:"required,description=Date in YYYY-MM-DD format"`
  }

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	// Define each tool as a handler function. Returning an error sends the
  	// message back to Claude as a tool result with is_error set.
  	createCalendarEvent, err := toolrunner.NewBetaToolFromJSONSchema(
  		"create_calendar_event",
  		"Create a calendar event with attendees and optional recurrence.",
  		func(ctx context.Context, input CreateCalendarEventInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
  			if len(input.Attendees) > 10 {
  				return anthropic.BetaToolResultBlockParamContentUnion{}, fmt.Errorf("too many attendees (max 10)")
  			}
  			return anthropic.BetaToolResultBlockParamContentUnion{
  				OfText: &anthropic.BetaTextBlockParam{
  					Text: fmt.Sprintf(`{"event_id": "evt_123", "status": "created", "title": %q}`, input.Title),
  				},
  			}, nil
  		},
  	)
  	if err != nil {
  		log.Fatal(err)
  	}

  	listCalendarEvents, err := toolrunner.NewBetaToolFromJSONSchema(
  		"list_calendar_events",
  		"List all calendar events on a given date.",
  		func(ctx context.Context, input ListCalendarEventsInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
  			return anthropic.BetaToolResultBlockParamContentUnion{
  				OfText: &anthropic.BetaTextBlockParam{
  					Text: `{"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}`,
  				},
  			}, nil
  		},
  	)
  	if err != nil {
  		log.Fatal(err)
  	}

  	// The runner calls the API, runs requested tools, and feeds results back
  	// until Claude produces a final answer.
  	runner := client.Beta.Messages.NewToolRunner(
  		[]anthropic.BetaTool{createCalendarEvent, listCalendarEvents},
  		anthropic.BetaToolRunnerParams{
  			BetaMessageNewParams: anthropic.BetaMessageNewParams{
  				Model:     anthropic.ModelClaudeOpus5_5,
  				MaxTokens: 1024,
  				Messages: []anthropic.BetaMessageParam{
  					anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(
  						"Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.",
  					)),
  				},
  			},
  		},
  	)

  	var finalMessage *anthropic.BetaMessage
  	for message, err := range runner.All(ctx) {
  		if err != nil {
  			log.Fatal(err)
  		}
  		finalMessage = message
  	}

  	for _, block := range finalMessage.Content {
  		if block.Type == "text" {
  			fmt.Println(block.Text)
  		}
  	}
  }
  ```

  ```java Java
  // Ring 5: The Tool Runner SDK abstraction.

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.helpers.BetaToolRunner;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.fasterxml.jackson.annotation.JsonClassDescription;
  import com.fasterxml.jackson.annotation.JsonPropertyDescription;
  import java.util.List;
  import java.util.function.Supplier;

  // Define each tool as a class: the fields describe the input schema, and the
  // get() method holds the implementation. Throwing an exception sends the
  // message back to Claude as a tool result with is_error set.
  @JsonClassDescription("Create a calendar event with attendees.")
  static class CreateCalendarEvent implements Supplier<String> {
      @JsonPropertyDescription("Event title")
      public String title;

      @JsonPropertyDescription("Start time in ISO 8601 format")
      public String start;

      @JsonPropertyDescription("End time in ISO 8601 format")
      public String end;

      @JsonPropertyDescription("Email addresses to invite")
      public List<String> attendees;

      @Override
      public String get() {
          if (attendees != null && attendees.size() > 10) {
              throw new IllegalArgumentException("Too many attendees (max 10)");
          }
          return "{\"event_id\": \"evt_123\", \"status\": \"created\", \"title\": \"" + title + "\"}";
      }
  }

  @JsonClassDescription("List all calendar events on a given date.")
  static class ListCalendarEvents implements Supplier<String> {
      @JsonPropertyDescription("Date in YYYY-MM-DD format")
      public String date;

      @Override
      public String get() {
          return "{\"events\": [{\"title\": \"Existing meeting\", \"start\": \"14:00\", \"end\": \"15:00\"}]}";
      }
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // The runner calls the API, runs requested tools, and feeds results back
      // until Claude produces a final answer.
      BetaToolRunner runner = client.beta()
              .messages()
              .toolRunner(MessageCreateParams.builder()
                      .model(Model.CLAUDE_OPUS_5_5)
                      .maxTokens(1024)
                      .addBeta("structured-outputs-2025-11-13")
                      .addUserMessage("Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.")
                      .addTool(CreateCalendarEvent.class)
                      .addTool(ListCalendarEvents.class)
                      .build());

      BetaMessage finalMessage = null;
      for (BetaMessage message : runner) {
          finalMessage = message;
      }

      finalMessage.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  // Ring 5: The Tool Runner SDK abstraction.

  use Anthropic\Client;
  use Anthropic\Lib\Tools\BetaRunnableTool;
  use Anthropic\Messages\Model;

  $client = new Client();

  // Define each tool as a runnable tool: the definition carries the JSON Schema
  // and the run closure holds the implementation. Throwing an exception sends the
  // message back to Claude as a tool result with is_error set.
  $createCalendarEvent = new BetaRunnableTool(
      definition: [
          'name' => 'create_calendar_event',
          'description' => 'Create a calendar event with attendees and optional recurrence.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'title' => ['type' => 'string', 'description' => 'Event title'],
                  'start' => ['type' => 'string', 'description' => 'Start time in ISO 8601 format'],
                  'end' => ['type' => 'string', 'description' => 'End time in ISO 8601 format'],
                  'attendees' => [
                      'type' => 'array',
                      'items' => ['type' => 'string'],
                      'description' => 'Email addresses to invite',
                  ],
                  'recurrence' => [
                      'type' => 'object',
                      'properties' => [
                          'frequency' => ['enum' => ['daily', 'weekly', 'monthly']],
                          'count' => ['type' => 'integer', 'minimum' => 1],
                      ],
                  ],
              ],
              'required' => ['title', 'start', 'end'],
          ],
      ],
      run: function (array $input): string {
          if (count($input['attendees'] ?? []) > 10) {
              throw new InvalidArgumentException('Too many attendees (max 10)');
          }

          return json_encode([
              'event_id' => 'evt_123',
              'status' => 'created',
              'title' => $input['title'],
          ]);
      },
  );

  $listCalendarEvents = new BetaRunnableTool(
      definition: [
          'name' => 'list_calendar_events',
          'description' => 'List all calendar events on a given date.',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'date' => ['type' => 'string', 'description' => 'Date in YYYY-MM-DD format'],
              ],
              'required' => ['date'],
          ],
      ],
      run: fn (array $input): string => json_encode([
          'events' => [['title' => 'Existing meeting', 'start' => '14:00', 'end' => '15:00']],
      ]),
  );

  // The runner calls the API, runs requested tools, and feeds results back
  // until Claude produces a final answer.
  $runner = $client->beta->messages->toolRunner(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => 'Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts.',
          ],
      ],
      model: Model::CLAUDE_OPUS_5_5,
      tools: [$createCalendarEvent, $listCalendarEvents],
  );

  $finalMessage = null;
  foreach ($runner as $message) {
      $finalMessage = $message;
  }

  foreach ($finalMessage->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, "\n";
      }
  }
  ```

  ```ruby Ruby
  # Ring 5: The Tool Runner SDK abstraction.

  require "anthropic"

  client = Anthropic::Client.new

  # Define each tool as a class: a typed input model describes the schema, and
  # the call method holds the implementation. Raising an error sends the message
  # back to Claude as a tool result with is_error set.
  class RecurrenceInput < Anthropic::BaseModel
    optional :frequency, Anthropic::InputSchema::EnumOf["daily", "weekly", "monthly"],
             doc: "How often the event repeats"
    optional :count, Integer, doc: "Number of occurrences"
  end

  class CreateCalendarEventInput < Anthropic::BaseModel
    required :title, String, doc: "Event title"
    required :start, String, doc: "Start time in ISO 8601 format"
    required :end, String, doc: "End time in ISO 8601 format"
    optional :attendees, Anthropic::InputSchema::ArrayOf[String], doc: "Email addresses to invite"
    optional :recurrence, RecurrenceInput, doc: "Optional recurrence rule"
  end

  class CreateCalendarEvent < Anthropic::BaseTool
    doc "Create a calendar event with attendees and optional recurrence."
    input_schema CreateCalendarEventInput

    def call(input)
      raise ArgumentError, "Too many attendees (max 10)" if input.attendees && input.attendees.length > 10
      JSON.generate({event_id: "evt_123", status: "created", title: input.title})
    end
  end

  class ListCalendarEventsInput < Anthropic::BaseModel
    required :date, String, doc: "Date in YYYY-MM-DD format"
  end

  class ListCalendarEvents < Anthropic::BaseTool
    doc "List all calendar events on a given date."
    input_schema ListCalendarEventsInput

    def call(input)
      JSON.generate({events: [{title: "Existing meeting", start: "14:00", end: "15:00"}]})
    end
  end

  # The runner calls the API, runs requested tools, and feeds results back
  # until Claude produces a final answer.
  runner = client.beta.messages.tool_runner(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    tools: [CreateCalendarEvent.new, ListCalendarEvents.new],
    messages: [
      {
        role: "user",
        content: "Check what I have on Monday, March 30, 2026, then schedule a one-hour planning session that day that avoids any conflicts."
      }
    ]
  )

  final_message = nil
  runner.each_message { |message| final_message = message }

  final_message.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

**What to expect**

```text Output wrap
I checked your calendar for Monday, March 30 and found an existing meeting from 2pm to 3pm. I've scheduled the planning session for 10am to 11am to avoid the conflict.
```

The output is identical to Ring 3. The difference is in the code: roughly half the lines, no manual loop, and the schema lives next to the implementation.

## What you built

You started with a single hardcoded tool call and ended with a production-shaped agent that handles multiple tools, parallel calls, and errors, then collapsed all of that into the Tool Runner. Along the way you saw every piece of the tool-use protocol: `tool_use` blocks, `tool_result` blocks, `tool_use_id` matching, `stop_reason` checking, and `is_error` signaling.

## Next steps

<CardGroup>
  <Card href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools" title="Define tools">
    Schema specification and best practices.
  </Card>

  <Card href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner" title="Tool Runner">
    The full SDK abstraction reference.
  </Card>

  <Card href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use" title="Troubleshooting">
    Fix common tool-use errors.
  </Card>
</CardGroup>

---
title: Structured outputs
url: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
description: Get validated JSON results from agent workflows
featureMetadata:
  status: ga
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-sonnet-4-6
    - claude-sonnet-4-5-20250929
    - claude-opus-4-5-20251101
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
  supportedPlatforms:
    Claude API: ga
    Claude Platform on AWS: ga
    Amazon Bedrock:
      availability: ga
      note: On Amazon Bedrock, structured outputs are available on the legacy [Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy) integration for Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5, and not on [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock).
    Google Cloud: ga
    Microsoft Foundry: ga
---

Structured outputs constrain Claude's responses to follow a specific schema, ensuring valid, parseable output for downstream processing. Structured outputs provide two complementary features:

* **JSON outputs** (`output_config.format`): Get Claude's response in a specific JSON format, for example to extract data from images or text, generate structured reports, or format API responses. This page covers JSON outputs.
* **Strict tool use** (`strict: true`): Guarantee schema validation on tool names and inputs. See [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use).

You can use these features independently or [together in the same request](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#using-both-features-together).

## Why use structured outputs

Without structured outputs, Claude can generate malformed JSON responses or invalid tool inputs that break your applications. Even with careful prompting, you may encounter:

* Parsing errors from invalid JSON syntax
* Missing required fields
* Inconsistent data types
* Schema violations requiring error handling and retries

Structured outputs guarantee schema-compliant responses through constrained decoding:

* **Always valid:** No more `JSON.parse()` errors
* **Type safe:** Guaranteed field types and required fields
* **Reliable:** No retries needed for schema violations

## How it works

<Steps>
  <Step title="Define your schema">
    Describe the structure you want as a JSON schema or as a type in your language. The schema follows JSON Schema, with some [limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations).
  </Step>

  <Step title="Send it in output_config.format">
    The request carries the schema in `output_config.format` with `type: "json_schema"`. SDK helpers set this for you.
  </Step>

  <Step title="Read the response">
    Claude returns valid JSON that matches your schema in the response's text content block. SDK helpers parse it into your type.
  </Step>
</Steps>

## Usage

<Tabs>
  <Tab title="cURL">
    ```bash
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-opus-5-5",
        "max_tokens": 1024,
        "messages": [
          {
            "role": "user",
            "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
          }
        ],
        "output_config": {
          "format": {
            "type": "json_schema",
            "schema": {
              "type": "object",
              "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "plan_interest": {"type": "string"},
                "demo_requested": {"type": "boolean"}
              },
              "required": ["name", "email", "plan_interest", "demo_requested"],
              "additionalProperties": false
            }
          }
        }
      }'
    ```

    Claude returns JSON like this in the response's text content block:

    ```json Output
    {
      "name": "John Smith",
      "email": "john@example.com",
      "plan_interest": "Enterprise",
      "demo_requested": true
    }
    ```
  </Tab>

  <Tab title="CLI">
    ```bash
    ant messages create \
      --transform 'content.#(type=="text").text|@fromstr' \
      --format jsonl <<'YAML'
    model: claude-opus-5-5
    max_tokens: 1024
    messages:
      - role: user
        content: >-
          Extract the key information from this email: John Smith
          (john@example.com) is interested in our Enterprise plan and wants
          to schedule a demo for next Tuesday at 2pm.
    output_config:
      format:
        type: json_schema
        schema:
          type: object
          properties:
            name: {type: string}
            email: {type: string}
            plan_interest: {type: string}
            demo_requested: {type: boolean}
          required: [name, email, plan_interest, demo_requested]
          additionalProperties: false
    YAML
    ```

    To print only some properties of the JSON output, pass a [GJSON path](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/using#transform-output-with-gjson) to `--transform`.

    The example above outputs:

    ```text Output wrap
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise","demo_requested":true}
    ```
  </Tab>

  <Tab title="Python">
    ```python
    from pydantic import BaseModel
    # ...


    class ContactInfo(BaseModel):
        name: str
        email: str
        plan_interest: str
        demo_requested: bool


    client = Anthropic()

    response = client.messages.parse(
        model="claude-opus-5-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the key information from this email: "
                    "John Smith (john@example.com) is interested in our Enterprise plan "
                    "and wants to schedule a demo for next Tuesday at 2pm."
                ),
            }
        ],
        output_format=ContactInfo,
    )

    print(response.parsed_output)
    ```

    Pass a [Pydantic](https://docs.pydantic.dev/) model to `client.messages.parse()`, the recommended method, as `output_format`. The SDK transforms the model's schema, sends it as `output_config.format`, validates the response, and returns the parsed model in `parsed_output`.

    The example above outputs:

    ```text Output wrap
    name='John Smith' email='john@example.com' plan_interest='Enterprise' demo_requested=True
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import { z } from "zod";
    import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

    const ContactInfoSchema = z.object({
      name: z.string(),
      email: z.string(),
      plan_interest: z.string(),
      demo_requested: z.boolean()
    });

    const client = new Anthropic();

    const response = await client.messages.parse({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content:
            "Extract the key information from this email: " +
            "John Smith (john@example.com) is interested in our Enterprise plan " +
            "and wants to schedule a demo for next Tuesday at 2pm."
        }
      ],
      output_config: { format: zodOutputFormat(ContactInfoSchema) }
    });

    // Automatically parsed and validated
    console.log(response.parsed_output);
    ```

    Wrap a [Zod](https://zod.dev/) schema in `zodOutputFormat()` and pass it to `client.messages.parse()` as `output_config.format`. `zodOutputFormat()` transforms the schema, and `parse()` validates the response and returns the parsed result in `parsed_output`, typed to match the schema.

    The example above outputs:

    ```javascript Output
    {
      name: 'John Smith',
      email: 'john@example.com',
      plan_interest: 'Enterprise',
      demo_requested: true
    }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic;
    using Anthropic.Models.Messages;
    using Anthropic.Services;

    var client = new AnthropicClient();

    var response = await client.Messages.Create<ContactInfo>(new MessageCreateParams
    {
        Model = Model.ClaudeOpus5_5,
        MaxTokens = 1024,
        Messages = [new() {
            Role = Role.User,
            Content = "Extract the key information from this email: "
                + "John Smith (john@example.com) is interested in our Enterprise plan "
                + "and wants to schedule a demo for next Tuesday at 2pm."
        }],
    });

    if (response.Content.Select(block => block.Parsed()).OfType<ContactInfo>().FirstOrDefault() is { } contact)
    {
        Console.WriteLine(contact);
    }

    public record ContactInfo
    {
        public string Name { get; set; } = "";
        public string Email { get; set; } = "";
        public string PlanInterest { get; set; } = "";
        public bool DemoRequested { get; set; }
    }
    ```

    Pass a plain C# class or record to the generic `Create<T>()` overload. The SDK derives a JSON schema from the type, transforms it, and parses each text block back into it.

    The example above outputs:

    ```text Output wrap
    ContactInfo { Name = John Smith, Email = john@example.com, PlanInterest = Enterprise, DemoRequested = True }
    ```
  </Tab>

  <Tab title="Go">
    ```go
    type ContactInfo struct {
    	Name          string `json:"name"`
    	Email         string `json:"email"`
    	PlanInterest  string `json:"plan_interest"`
    	DemoRequested bool   `json:"demo_requested"`
    }

    func main() {
    	client := anthropic.NewClient()

    	var contact ContactInfo
    	_, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
    		Model:     anthropic.ModelClaudeOpus5_5,
    		MaxTokens: 1024,
    		Messages: []anthropic.BetaMessageParam{
    			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(
    				"Extract the key information from this email: " +
    					"John Smith (john@example.com) is interested in our Enterprise plan " +
    					"and wants to schedule a demo for next Tuesday at 2pm.",
    			)),
    		},
    		OutputConfig: anthropic.BetaOutputConfigParam{
    			Format: anthropic.BetaJSONOutputFormatParam{Schema: &contact},
    		},
    	})
    	if err != nil {
    		panic(err)
    	}

    	fmt.Printf("%#v\n", contact)
    }
    ```

    <Note>
      Passing a struct as the schema is in beta in Go, so this example uses `client.Beta.Messages.New`. To use the GA `client.Messages.New`, pass a JSON schema as shown in [Using a raw JSON schema](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#using-a-raw-json-schema).
    </Note>

    The SDK generates and transforms the JSON schema from the struct and unmarshals the response into it.

    The example above outputs:

    ```text Output wrap
    main.ContactInfo{Name:"John Smith", Email:"john@example.com", PlanInterest:"Enterprise", DemoRequested:true}
    ```
  </Tab>

  <Tab title="Java">
    ```java
    static class ContactInfo {
        public String name;
        public String email;
        public String plan_interest;
        public boolean demo_requested;
    }

    void main() throws Exception {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_5_5)
            .maxTokens(1024)
            .addUserMessage("Extract the key information from this email: "
                + "John Smith (john@example.com) is interested in our Enterprise plan "
                + "and wants to schedule a demo for next Tuesday at 2pm.")
            .outputConfig(ContactInfo.class)
            .build();

        StructuredMessage<ContactInfo> response = client.messages().create(params);
        ContactInfo contact = response.content().stream()
            .flatMap(block -> block.text().stream())
            .findFirst().orElseThrow().text();
        IO.println(new ObjectMapper().writeValueAsString(contact));
    }
    ```

    When you pass a Java class to `outputConfig()`, the SDK derives a JSON schema from it and validates the schema. The builder then produces a `StructuredMessageCreateParams<T>`. Rather than transforming the schema, the SDK's local validation rejects [constraints not supported by the API](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations). Read the parsed result with `response.content().stream().flatMap(block -> block.text().stream()).findFirst().orElseThrow().text()`.

    The example above outputs:

    ```text Output wrap
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise","demo_requested":true}
    ```

    <Note>
      Declare your schema classes as top-level classes or `static` nested classes. This requirement comes from the Jackson Databind library (`com.fasterxml.jackson.databind`), which the SDK uses to deserialize JSON responses into your class instances and cannot instantiate non-static inner classes.
    </Note>

    <Accordion title="Generic type erasure">
      Java retains generic type information for fields in the class's metadata, but generic type erasure applies in other scopes. While a JSON schema can be derived from a `BookList.books` field with type `List<Book>`, a valid JSON schema cannot be derived from a local variable of that same type.

      If an error occurs while converting a JSON response to a Java class instance, the error message includes the JSON response to assist in diagnosis. If your JSON response may contain sensitive information, avoid logging it directly, or ensure that you redact any sensitive details from the error message.
    </Accordion>

    <Accordion title="Local schema validation">
      Structured outputs support a [subset of the JSON Schema language](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations). The SDK generates schemas automatically from classes to align with this subset. The `outputConfig(Class<T>)` method performs a validation check on the schema derived from the specified class.

      Key points:

      * **Local validation** occurs without sending requests to the remote AI model.
      * **Remote validation** is also performed by the AI model upon receiving the JSON schema.
      * **Version compatibility:** Local validation may fail while remote validation succeeds if the SDK version is outdated.
      * **Disabling local validation:** Pass `JsonSchemaLocalValidation.NO` if you encounter compatibility issues:

      ```java
      import com.anthropic.core.JsonSchemaLocalValidation;
      // ...

      static class BookList {
          public List<String> books;
      }

      void main() {
          StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(2048)
              .outputConfig(BookList.class, JsonSchemaLocalValidation.NO)
              .addUserMessage("List some famous late twentieth century novels.")
              .build();
      }
      ```
    </Accordion>

    <Accordion title="Streaming">
      Structured outputs also work with streaming. As responses arrive in stream events, you need to accumulate the full response before deserializing the JSON.

      Use `MessageAccumulator` to collect the JSON strings from the stream. Once accumulated, call `MessageAccumulator.message(Class<T>)` to convert the accumulated `Message` into a `StructuredMessage`, which automatically deserializes the JSON into your Java class.
    </Accordion>

    <Accordion title="JSON schema properties">
      When the SDK derives a JSON schema from your Java classes, it includes all properties represented by `public` fields or `public` getter methods by default and excludes non-`public` fields and getter methods.

      You can control visibility with annotations:

      * `@JsonIgnore` excludes a `public` field or getter method
      * `@JsonProperty` includes a non-`public` field or getter method

      If you define `private` fields with `public` getter methods, the SDK derives the property name from the getter (for example, `private` field `myValue` with `public` method `getMyValue()` produces a `"myValue"` property). To use a non-conventional getter name, annotate the method with `@JsonProperty`.

      Each class must define at least one property for the JSON schema. A validation error occurs if no fields or getter methods can produce schema properties, such as when:

      * There are no fields or getter methods in the class
      * All `public` members are annotated with `@JsonIgnore`
      * All non-`public` members lack `@JsonProperty` annotations
      * A field uses a `Map` type, which produces an empty `"properties"` field
    </Accordion>

    <Accordion title="Composition and inheritance">
      Your Java classes can use composition and inheritance to share structure when defining JSON schemas. Each pattern affects the output structure differently.

      **Composition** produces nested JSON output. Deriving a schema from class `Composed` that composes `A` and `B`:

      ```java
      static class A {
          public String a;
      }

      static class B {
          public String b;
      }

      static class Composed {
          public A composedA;
          public B composedB;
      }
      ```

      The JSON output has this nested structure:

      ```json
      {
        "composedA": { "a": "hello" },
        "composedB": { "b": "world" }
      }
      ```

      **Inheritance** produces flat JSON output. Deriving a schema from class `Derived` that extends `Base`:

      ```java
      static class Base {
          public String a;
      }

      static class Derived extends Base {
          public String b;
      }
      ```

      The JSON output has this flat structure:

      ```json
      {
        "a": "hello",
        "b": "world"
      }
      ```
    </Accordion>

    <Accordion title="Annotations (Jackson and Swagger)">
      You can use Jackson Databind annotations to enrich the JSON schema derived from your Java classes:

      ```java
      import com.fasterxml.jackson.annotation.JsonClassDescription;
      import com.fasterxml.jackson.annotation.JsonIgnore;
      import com.fasterxml.jackson.annotation.JsonPropertyDescription;

      static class Person {

        @JsonPropertyDescription("The first name and surname of the person")
        public String name;

        public int birthYear;

        @JsonPropertyDescription("The year the person died, or 'present' if the person is living.")
        public String deathYear;
      }

      @JsonClassDescription("The details of one published book")
      static class Book {

        public String title;
        public Person author;

        @JsonPropertyDescription("The year in which the book was first published.")
        public int publicationYear;

        @JsonIgnore
        public String genre;
      }

      static class BookList {
        public List<Book> books;
      }
      ```

      Annotation summary:

      * `@JsonClassDescription`: Add a description to a class
      * `@JsonPropertyDescription`: Add a description to a field or getter method
      * `@JsonIgnore`: Exclude a `public` field or getter from the schema
      * `@JsonProperty`: Include a non-`public` field or getter in the schema

      If you use `@JsonProperty(required = false)`, the SDK ignores the `false` value. Class-derived schemas always mark all properties as required.

      You can also use Swagger Core (OpenAPI 3) `@Schema` and `@ArraySchema` annotations for type-specific constraints:

      ```java
      import io.swagger.v3.oas.annotations.media.ArraySchema;
      import io.swagger.v3.oas.annotations.media.Schema;

      static class Article {

        @ArraySchema(minItems = 1)
        public List<String> authors;

        public String title;

        @Schema(format = "date")
        public String publicationDate;

        public int pageCount;
      }
      ```

      Local validation checks that you haven't used any unsupported constraint keywords, but constraint values aren't validated locally. For example, an unsupported `"format"` value may pass local validation but cause a remote error.

      If you use both Jackson and Swagger annotations to set the same schema field, the Jackson annotation takes precedence.
    </Accordion>
  </Tab>

  <Tab title="PHP">
    ```php
    use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
    use Anthropic\Lib\Contracts\StructuredOutputModel;

    $client = new Client();

    class ContactInfo implements StructuredOutputModel
    {
        use StructuredOutputModelTrait;

        public string $name;
        public string $email;
        public string $plan_interest;
        public bool $demo_requested;
    }

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            [
                'role' => 'user',
                'content' => 'Extract the key information from this email: '
                    . 'John Smith (john@example.com) is interested in our Enterprise plan '
                    . 'and wants to schedule a demo for next Tuesday at 2pm.',
            ],
        ],
        model: 'claude-opus-5-5',
        outputConfig: ['format' => ContactInfo::class],
    );

    $contact = $message->parsedOutput();
    if ($contact instanceof ContactInfo) {
        var_dump($contact);
    }
    ```

    Define a class that implements `StructuredOutputModel` and uses `StructuredOutputModelTrait`, and pass its name in `outputConfig: ['format' => MyClass::class]`. The SDK derives a JSON schema from the class's PHP 8 property types, transforms it, and returns a typed instance from `$message->parsedOutput()`.

    `parsedOutput()` returns your model instance on success, or `null` (or an error array) if parsing fails. Use `instanceof` to narrow the type before accessing fields.

    The example above outputs:

    ```text Output wrap
    object(ContactInfo)#42 (4) {
      ["name"]=>
      string(10) "John Smith"
      ["email"]=>
      string(16) "john@example.com"
      ["plan_interest"]=>
      string(10) "Enterprise"
      ["demo_requested"]=>
      bool(true)
    }
    ```

    <Accordion title="Type inference">
      The SDK maps native PHP 8 property types to JSON Schema:

      | PHP type                                   | JSON Schema                        |
      | ------------------------------------------ | ---------------------------------- |
      | `string`                                   | `"string"`                         |
      | `int`                                      | `"integer"`                        |
      | `float`                                    | `"number"`                         |
      | `bool`                                     | `"boolean"`                        |
      | `array`                                    | `"array"` (see the following note) |
      | `?type` (nullable)                         | Optional field                     |
      | Class implementing `StructuredOutputModel` | Nested object                      |

      For `array` properties, the SDK adds an `items` schema only when the element type is a nested `StructuredOutputModel`, declared with `#[Constrained(itemClass: MyModel::class)]` or a `/** @var MyModel[] */` docblock. Arrays of scalars (`string[]`, `int[]`) emit an unconstrained `{"type":"array"}`.

      All non-nullable properties become required fields.
    </Accordion>

    <Accordion title="Constraints with the #[Constrained] attribute">
      Add constraints with the `#[Constrained]` attribute:

      ```php
      use Anthropic\Lib\Attributes\Constrained;
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      class Address implements StructuredOutputModel { use StructuredOutputModelTrait; public string $street; }

      class Profile implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          #[Constrained(description: 'Age in years', minimum: 0, maximum: 150)]
          public int $age;

          #[Constrained(format: 'email')]
          public string $email;

          #[Constrained(itemClass: Address::class, minItems: 1)]
          public array $addresses;
      }
      ```

      **API-enforced constraints** (sent in the schema): `description`, `format`, `const`, `itemClass`, `minItems` (0 or 1 only).

      **SDK-validated constraints** (stripped from the wire schema, appended to the description, and validated against the response): `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`.
    </Accordion>
  </Tab>

  <Tab title="Ruby">
    ```ruby
    client = Anthropic::Client.new

    class ContactInfo < Anthropic::BaseModel
      required :name, String
      required :email, String
      required :plan_interest, String
      required :demo_requested, Anthropic::Boolean
    end

    message = client.messages.create(
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [{
        role: "user",
        content: "Extract the key information from this email: " \
          "John Smith (john@example.com) is interested in our Enterprise plan " \
          "and wants to schedule a demo for next Tuesday at 2pm."
      }],
      output_config: {format: ContactInfo}
    )

    contact = message.parsed_output
    puts contact
    ```

    Define a class that extends `Anthropic::BaseModel` and pass it to `messages.create()` as `output_config: {format: Model}`. The SDK derives a JSON schema from the class, transforms it, and assigns the parsed result to the response's `parsed_output` attribute as a typed Ruby object.

    The example above outputs:

    ```text Output wrap
    {name: "John Smith", email: "john@example.com", plan_interest: "Enterprise", demo_requested: true}
    ```

    <Accordion title="Advanced model features">
      The Ruby SDK supports additional model definition features for richer schemas:

      * **`doc:` keyword:** Add descriptions to fields for more informative schema output
      * **`Anthropic::ArrayOf[T]`:** Typed arrays. Pass array-level constraints (`min_items:`, `max_items:`) as keywords on `required`/`optional`, not on `ArrayOf` itself
      * **`Anthropic::EnumOf[:a, :b]`:** Enum fields with constrained values
      * **`Anthropic::UnionOf[T1, T2]`:** Union types mapped to `anyOf`

      ```ruby
      class FamousNumber < Anthropic::BaseModel
        required :value, Float
        optional :reason, String, doc: "why is this number mathematically significant?"
      end

      class Output < Anthropic::BaseModel
        required :numbers, Anthropic::ArrayOf[FamousNumber], min_items: 3, max_items: 5
      end

      message = client.messages.create(
        model: "claude-opus-5-5",
        max_tokens: 1024,
        messages: [{role: "user", content: "give me some famous numbers"}],
        output_config: {format: Output}
      )

      message.parsed_output
      # => #<Output numbers=[#<FamousNumber value=3.14159... reason="Pi is...">...]>
      ```
    </Accordion>
  </Tab>
</Tabs>

## How SDK transformation works

Most SDK helpers transform schemas that use unsupported features. The transformation steps:

1. **Remove unsupported constraints** (for example, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Update descriptions** by adding each unsupported constraint to the field's description (for example, `{minimum: 100}`)
3. **Add `additionalProperties: false`** to all objects
4. **Filter string formats** to supported list only
5. **Validate responses** against your original schema and all its constraints, if the helper validates responses

Claude receives a simplified schema, but a helper that validates responses still enforces every constraint in your code.

**Example:** A field with `minimum: 100` becomes a plain integer in the sent schema, and the SDK adds `{minimum: 100}` to the field's description. A helper that validates responses still checks the response against `minimum: 100`.

## Using a raw JSON schema

To use a JSON schema from a file, an OpenAPI spec, or code that builds it at runtime, pass it in `output_config.format`.

<Tabs>
  <Tab title="cURL">
    ```bash
    curl https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "claude-opus-5-5",
        "max_tokens": 1024,
        "messages": [
          {
            "role": "user",
            "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
          }
        ],
        "output_config": {
          "format": {
            "type": "json_schema",
            "schema": {
              "type": "object",
              "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "plan_interest": {"type": "string"},
                "demo_requested": {"type": "boolean"}
              },
              "required": ["name", "email", "plan_interest", "demo_requested"],
              "additionalProperties": false
            }
          }
        }
      }'
    ```

    Claude returns JSON like this in the response's text content block:

    ```json Output
    {
      "name": "John Smith",
      "email": "john@example.com",
      "plan_interest": "Enterprise",
      "demo_requested": true
    }
    ```
  </Tab>

  <Tab title="CLI">
    ```bash
    ant messages create \
      --transform 'content.#(type=="text").text|@fromstr' \
      --format jsonl <<'YAML'
    model: claude-opus-5-5
    max_tokens: 1024
    messages:
      - role: user
        content: >-
          Extract the key information from this email: John Smith
          (john@example.com) is interested in our Enterprise plan and wants
          to schedule a demo for next Tuesday at 2pm.
    output_config:
      format:
        type: json_schema
        schema:
          type: object
          properties:
            name: {type: string}
            email: {type: string}
            plan_interest: {type: string}
            demo_requested: {type: boolean}
          required: [name, email, plan_interest, demo_requested]
          additionalProperties: false
    YAML
    ```

    The example above outputs:

    ```text Output wrap
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise","demo_requested":true}
    ```
  </Tab>

  <Tab title="Python">
    ```python
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the key information from this email: "
                    "John Smith (john@example.com) is interested in our Enterprise plan "
                    "and wants to schedule a demo for next Tuesday at 2pm."
                ),
            }
        ],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "plan_interest": {"type": "string"},
                        "demo_requested": {"type": "boolean"},
                    },
                    "required": ["name", "email", "plan_interest", "demo_requested"],
                    "additionalProperties": False,
                },
            }
        },
    )
    text = next(block.text for block in response.content if block.type == "text")
    contact = json.loads(text)
    print(contact)
    ```

    The example above outputs:

    ```text Output wrap
    {'name': 'John Smith', 'email': 'john@example.com', 'plan_interest': 'Enterprise', 'demo_requested': True}
    ```

    To move [constraints not supported by the API](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations) into field descriptions, pass the schema through `transform_schema()` from the `anthropic` package before sending it, and edit the result if you need to. `transform_schema()` also accepts a Pydantic model. Unlike `client.messages.parse()`, it returns the transformed schema rather than sending it.
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import { jsonSchemaOutputFormat } from "@anthropic-ai/sdk/helpers/json-schema";

    const client = new Anthropic();

    const response = await client.messages.parse({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
        }
      ],
      output_config: {
        format: jsonSchemaOutputFormat({
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            planInterest: { type: "string" }
          },
          required: ["name", "email", "planInterest"],
          additionalProperties: false
        } as const)
      }
    });

    // response.parsed_output is typed as { name: string; email: string; planInterest: string } | null
    console.log(response.parsed_output);
    ```

    Use `jsonSchemaOutputFormat()` to pass a plain JSON schema to `parse()`, without installing Zod. The API returns a response that conforms to the schema, and if you declare the schema with `as const`, the type for `parsed_output` is automatically inferred by TypeScript according to your schema. For an imported or generated schema, `parsed_output` is typed as `unknown`.

    By default, the helper [transforms the schema](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#how-sdk-transformation-works) the same way `zodOutputFormat()` does. Pass `{ transform: false }` as the second argument to send it unchanged. Unlike `zodOutputFormat()`, it doesn't validate the response, so it won't catch violations of [constraints not supported by the API](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations), such as `minimum`.

    The example above outputs:

    ```javascript Output
    { name: 'John Smith', email: 'john@example.com', planInterest: 'Pro' }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using System.Text.Json;
    using Anthropic;
    using Anthropic.Models.Messages;

    var client = new AnthropicClient();

    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus5_5,
        MaxTokens = 1024,
        Messages = [new() {
            Role = Role.User,
            Content = "Extract the key information from this email: "
                + "John Smith (john@example.com) is interested in our Enterprise plan "
                + "and wants to schedule a demo for next Tuesday at 2pm."
        }],
        OutputConfig = new OutputConfig
        {
            Format = new JsonOutputFormat
            {
                Schema = new Dictionary<string, JsonElement>
                {
                    ["type"] = JsonSerializer.SerializeToElement("object"),
                    ["properties"] = JsonSerializer.SerializeToElement(new
                    {
                        name = new { type = "string" },
                        email = new { type = "string" },
                        plan_interest = new { type = "string" },
                        demo_requested = new { type = "boolean" },
                    }),
                    ["required"] = JsonSerializer.SerializeToElement(
                        new[] { "name", "email", "plan_interest", "demo_requested" }),
                    ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                },
            },
        },
    });

    if (response.Content.Select(b => b.Value).OfType<TextBlock>().FirstOrDefault() is { } textBlock)
    {
        // JSON is guaranteed to match the schema
        var contact = JsonSerializer.Deserialize<JsonElement>(textBlock.Text);
        Console.WriteLine(contact);
    }
    ```

    The example above outputs:

    ```text Output wrap
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise","demo_requested":true}
    ```
  </Tab>

  <Tab title="Go">
    ```go
    type ContactInfo struct {
    	Name          string `json:"name"`
    	Email         string `json:"email"`
    	PlanInterest  string `json:"plan_interest"`
    	DemoRequested bool   `json:"demo_requested"`
    }

    func main() {
    	client := anthropic.NewClient()

    	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus5_5,
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock(
    				"Extract the key information from this email: " +
    					"John Smith (john@example.com) is interested in our Enterprise plan " +
    					"and wants to schedule a demo for next Tuesday at 2pm.",
    			)),
    		},
    		OutputConfig: anthropic.OutputConfigParam{
    			Format: anthropic.JSONOutputFormatParam{
    				Schema: map[string]any{
    					"type": "object",
    					"properties": map[string]any{
    						"name":           map[string]string{"type": "string"},
    						"email":          map[string]string{"type": "string"},
    						"plan_interest":  map[string]string{"type": "string"},
    						"demo_requested": map[string]string{"type": "boolean"},
    					},
    					"required":             []string{"name", "email", "plan_interest", "demo_requested"},
    					"additionalProperties": false,
    				},
    			},
    		},
    	})

    	for _, block := range message.Content {
    		switch variant := block.AsAny().(type) {
    		case anthropic.TextBlock:
    			var contact ContactInfo
    			json.Unmarshal([]byte(variant.Text), &contact)
    			fmt.Printf("%#v\n", contact)
    		}
    	}
    }
    ```

    The example above outputs:

    ```text Output wrap
    main.ContactInfo{Name:"John Smith", Email:"john@example.com", PlanInterest:"Enterprise", DemoRequested:true}
    ```

    To have the SDK transform a map schema, pass it through `BetaJSONSchemaOutputFormat()` on the beta API.
  </Tab>

  <Tab title="Java">
    ```java
    import com.anthropic.core.JsonValue;
    import com.anthropic.models.messages.JsonOutputFormat;
    // ...
    import com.anthropic.models.messages.OutputConfig;
    import com.fasterxml.jackson.databind.JsonNode;
    import com.fasterxml.jackson.databind.ObjectMapper;

    void main() throws Exception {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        JsonOutputFormat.Schema schema = JsonOutputFormat.Schema.builder()
            .putAdditionalProperty("type", JsonValue.from("object"))
            .putAdditionalProperty("properties", JsonValue.from(Map.of(
                "name", Map.of("type", "string"),
                "email", Map.of("type", "string"),
                "plan_interest", Map.of("type", "string"))))
            .putAdditionalProperty("required", JsonValue.from(
                List.of("name", "email", "plan_interest")))
            .putAdditionalProperty("additionalProperties", JsonValue.from(false))
            .build();

        OutputConfig outputConfig = OutputConfig.builder()
            .format(JsonOutputFormat.builder().schema(schema).build())
            .build();

        MessageCreateParams createParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_5_5)
            .maxTokens(1024)
            .outputConfig(outputConfig)
            .addUserMessage(
                "John Smith (john@example.com) is interested in our Enterprise plan.")
            .build();

        String json = client.messages().create(createParams).content().stream()
            .flatMap(contentBlock -> contentBlock.text().stream())
            .findFirst()
            .orElseThrow()
            .text();

        JsonNode contact = new ObjectMapper().readTree(json);
        IO.println(contact);
    }
    ```

    The example above outputs:

    ```text Output wrap
    {"name":"John Smith","email":"john@example.com","plan_interest":"Enterprise"}
    ```

    For a more extensive example that builds a nested schema with arrays and descriptions, see [`StructuredOutputsRawExample.java`](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/StructuredOutputsRawExample.java) in the SDK repository.
  </Tab>

  <Tab title="PHP">
    ```php
    use Anthropic\Messages\OutputConfig;
    use Anthropic\Messages\JSONOutputFormat;

    $client = new Client();

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            [
                'role' => 'user',
                'content' => 'Extract the key information from this email: '
                    . 'John Smith (john@example.com) is interested in our Enterprise plan.',
            ],
        ],
        model: 'claude-opus-5-5',
        outputConfig: OutputConfig::with(format: JSONOutputFormat::with(schema: [
            'type' => 'object',
            'properties' => [
                'name' => ['type' => 'string'],
                'email' => ['type' => 'string'],
                'plan_interest' => ['type' => 'string'],
            ],
            'required' => ['name', 'email', 'plan_interest'],
            'additionalProperties' => false,
        ])),
    );

    $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
    $contact = json_decode($textBlock->text, associative: true);
    var_dump($contact);
    ```

    Pass the schema as an associative array to `OutputConfig::with()`, and decode the response with `json_decode()`.

    The example above outputs:

    ```text Output wrap
    array(3) {
      ["name"]=>
      string(10) "John Smith"
      ["email"]=>
      string(16) "john@example.com"
      ["plan_interest"]=>
      string(10) "Enterprise"
    }
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    client = Anthropic::Client.new

    response = client.messages.create(
      model: "claude-opus-5-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract the key information from this email: " \
            "John Smith (john@example.com) is interested in our Enterprise plan " \
            "and wants to schedule a demo for next Tuesday at 2pm."
        }
      ],
      output_config: {
        format: {
          type: "json_schema",
          schema: {
            type: "object",
            properties: {
              name: { type: "string" },
              email: { type: "string" },
              plan_interest: { type: "string" },
              demo_requested: { type: "boolean" }
            },
            required: ["name", "email", "plan_interest", "demo_requested"],
            additionalProperties: false
          }
        }
      }
    )

    text = response.content.find { it.type == :text }.text
    contact = JSON.parse(text)
    p contact
    ```

    The example above outputs:

    ```text Output wrap
    {"name" => "John Smith", "email" => "john@example.com", "plan_interest" => "Enterprise", "demo_requested" => true}
    ```
  </Tab>
</Tabs>

## Common use cases

<AccordionGroup>
  <Accordion title="Data extraction">
    Extract structured data from unstructured text:

    <CodeGroup>
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 4096,
          "messages": [
            {
              "role": "user",
              "content": "Extract invoice data from: Invoice #12345, Date: 2024-01-15, Total: $500.00"
            }
          ],
          "output_config": {
            "format": {
              "type": "json_schema",
              "schema": {
                "type": "object",
                "properties": {
                  "invoice_number": {"type": "string"},
                  "date": {"type": "string"},
                  "total_amount": {"type": "number"},
                  "line_items": {
                    "type": "array",
                    "items": {"type": "object", "additionalProperties": false}
                  },
                  "customer_name": {"type": "string"}
                },
                "required": ["invoice_number", "date", "total_amount", "line_items", "customer_name"],
                "additionalProperties": false
              }
            }
          }
        }'
      ```

      ```bash CLI
      ant messages create \
        --transform 'content.#(type=="text").text|@fromstr' \
        --format jsonl <<'YAML'
      model: claude-opus-5-5
      max_tokens: 4096
      messages:
        - role: user
          content: "Extract invoice data from: Invoice #12345, Date: 2024-01-15, Total: $500.00"
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              invoice_number: {type: string}
              date: {type: string}
              total_amount: {type: number}
              line_items:
                type: array
                items: {type: object, additionalProperties: false}
              customer_name: {type: string}
            required: [invoice_number, date, total_amount, line_items, customer_name]
            additionalProperties: false
      YAML
      ```

      ```python Python
      from pydantic import BaseModel


      class Invoice(BaseModel):
          invoice_number: str
          date: str
          total_amount: float
          line_items: list[dict]
          customer_name: str


      client = anthropic.Anthropic()
      invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      response = client.messages.parse(
          model="claude-opus-5-5",
          max_tokens=4096,
          output_format=Invoice,
          messages=[
              {"role": "user", "content": f"Extract invoice data from: {invoice_text}"}
          ],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const InvoiceSchema = z.object({
        invoice_number: z.string(),
        date: z.string(),
        total_amount: z.number(),
        line_items: z.array(z.record(z.string(), z.any())),
        customer_name: z.string()
      });

      const invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";
      const response = await client.messages.parse({
        model: "claude-opus-5-5",
        max_tokens: 4096,
        output_config: { format: zodOutputFormat(InvoiceSchema) },
        messages: [{ role: "user", content: `Extract invoice data from: ${invoiceText}` }]
      });
      console.log(response.parsed_output);
      ```

      ```csharp C#
      AnthropicClient client = new();

      string invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 4096,
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          invoice_number = new { type = "string" },
                          date = new { type = "string" },
                          total_amount = new { type = "number" },
                          line_items = new
                          {
                              type = "array",
                              items = new
                              {
                                  type = "object",
                                  additionalProperties = false,
                              },
                          },
                          customer_name = new { type = "string" },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "invoice_number", "date", "total_amount", "line_items", "customer_name" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
          Messages = [new() { Role = Role.User, Content = $"Extract invoice data from: {invoiceText}" }]
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      invoiceText := "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      schema := map[string]any{
      	"type":                 "object",
      	"additionalProperties": false,
      	"properties": map[string]any{
      		"invoice_number": map[string]any{"type": "string"},
      		"date":           map[string]any{"type": "string"},
      		"total_amount":   map[string]any{"type": "number"},
      		"line_items": map[string]any{
      			"type": "array",
      			"items": map[string]any{
      				"type":                 "object",
      				"additionalProperties": false,
      				"properties": map[string]any{
      					"description": map[string]any{"type": "string"},
      					"quantity":    map[string]any{"type": "number"},
      					"unit_price":  map[string]any{"type": "number"},
      				},
      				"required": []string{"description", "quantity", "unit_price"},
      			},
      		},
      		"customer_name": map[string]any{"type": "string"},
      	},
      	"required": []string{"invoice_number", "date", "total_amount", "line_items", "customer_name"},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus5_5,
      	MaxTokens: 4096,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: schema,
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Extract invoice data from: %s", invoiceText))),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		fmt.Println(variant.Text)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class LineItem {
          @JsonProperty("description")
          public String description;

          @JsonProperty("quantity")
          public int quantity;

          @JsonProperty("unit_price")
          public double unitPrice;
      }

      static class Invoice {
          @JsonProperty("invoice_number")
          public String invoiceNumber;

          @JsonProperty("date")
          public String date;

          @JsonProperty("total_amount")
          public double totalAmount;

          @JsonProperty("line_items")
          public List<LineItem> lineItems;

          @JsonProperty("customer_name")
          public String customerName;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

          StructuredMessageCreateParams<Invoice> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(4096L)
              .outputConfig(Invoice.class)
              .addUserMessage("Extract invoice data from: " + invoiceText)
              .build();

          StructuredMessage<Invoice> response = client.messages().create(params);
          Invoice invoice = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(invoice.invoiceNumber + ": $" + invoice.totalAmount);
      }
      ```

      ```php PHP
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Invoice implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $invoice_number;
          public string $date;
          public float $total_amount;
          public array $line_items;
          public string $customer_name;
      }

      $invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

      $message = $client->messages->create(
          maxTokens: 4096,
          messages: [
              ['role' => 'user', 'content' => "Extract invoice data from: $invoiceText"]
          ],
          model: 'claude-opus-5-5',
          outputConfig: ['format' => Invoice::class],
      );

      $invoice = $message->parsedOutput();
      if ($invoice instanceof Invoice) {
          echo "Invoice {$invoice->invoice_number}: \${$invoice->total_amount}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class LineItem < Anthropic::BaseModel
        required :description, String
        required :amount, Float
      end

      class Invoice < Anthropic::BaseModel
        required :invoice_number, String
        required :date, String
        required :total_amount, Float
        required :line_items, Anthropic::ArrayOf[LineItem]
        required :customer_name, String
      end

      invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      message = client.messages.create(
        model: "claude-opus-5-5",
        max_tokens: 4096,
        output_config: {format: Invoice},
        messages: [
          {role: "user", content: "Extract invoice data from: #{invoice_text}"}
        ]
      )

      invoice = message.parsed_output
      puts "Invoice #{invoice.invoice_number}: $#{invoice.total_amount}"
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Classification">
    Classify content with structured categories:

    <CodeGroup>
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 1024,
          "messages": [
            {
              "role": "user",
              "content": "Classify this feedback: Great product, fast shipping!"
            }
          ],
          "output_config": {
            "format": {
              "type": "json_schema",
              "schema": {
                "type": "object",
                "properties": {
                  "category": {"type": "string"},
                  "confidence": {"type": "number"},
                  "tags": {"type": "array", "items": {"type": "string"}},
                  "sentiment": {"type": "string"}
                },
                "required": ["category", "confidence", "tags", "sentiment"],
                "additionalProperties": false
              }
            }
          }
        }'
      ```

      ```bash CLI
      ant messages create \
        --transform 'content.#(type=="text").text|@fromstr' \
        --format jsonl <<'YAML'
      model: claude-opus-5-5
      max_tokens: 1024
      messages:
        - role: user
          content: "Classify this feedback: Great product, fast shipping!"
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              category:
                type: string
              confidence:
                type: number
              tags:
                type: array
                items:
                  type: string
              sentiment:
                type: string
            required:
              - category
              - confidence
              - tags
              - sentiment
            additionalProperties: false
      YAML
      ```

      ```python Python
      from pydantic import BaseModel

      client = Anthropic()


      class Classification(BaseModel):
          category: str
          confidence: float
          tags: list[str]
          sentiment: str


      feedback_text = "Great product, but the delivery was slow."
      response = client.messages.parse(
          model="claude-opus-5-5",
          max_tokens=1024,
          output_format=Classification,
          messages=[{"role": "user", "content": f"Classify this feedback: {feedback_text}"}],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const ClassificationSchema = z.object({
        category: z.string(),
        confidence: z.number(),
        tags: z.array(z.string()),
        sentiment: z.string()
      });

      const feedbackText = "Great product, but the delivery was slow.";
      const response = await client.messages.parse({
        model: "claude-opus-5-5",
        max_tokens: 1024,
        output_config: { format: zodOutputFormat(ClassificationSchema) },
        messages: [{ role: "user", content: `Classify this feedback: ${feedbackText}` }]
      });

      console.log(response.parsed_output);
      ```

      ```csharp C#
      string feedbackText = "Great product, fast shipping!";

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = $"Classify this feedback: {feedbackText}" }],
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          category = new { type = "string" },
                          confidence = new { type = "number" },
                          tags = new { type = "array", items = new { type = "string" } },
                          sentiment = new { type = "string" },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "category", "confidence", "tags", "sentiment" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      feedbackText := "Great product, fast shipping!"

      schema := map[string]any{
      	"type": "object",
      	"properties": map[string]any{
      		"category":   map[string]any{"type": "string"},
      		"confidence": map[string]any{"type": "number"},
      		"tags":       map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
      		"sentiment":  map[string]any{"type": "string"},
      	},
      	"required":             []string{"category", "confidence", "tags", "sentiment"},
      	"additionalProperties": false,
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus5_5,
      	MaxTokens: 1024,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: schema,
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Classify this feedback: %s", feedbackText))),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		var result map[string]any
      		json.Unmarshal([]byte(variant.Text), &result)
      		fmt.Println(result)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class Classification {
          @JsonProperty("category")
          public String category;

          @JsonProperty("confidence")
          public double confidence;

          @JsonProperty("tags")
          public List<String> tags;

          @JsonProperty("sentiment")
          public String sentiment;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String feedbackText = "Great product, fast shipping!";

          StructuredMessageCreateParams<Classification> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .outputConfig(Classification.class)
              .addUserMessage("Classify this feedback: " + feedbackText)
              .build();

          StructuredMessage<Classification> response = client.messages().create(params);
          Classification result = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(result.category + " (" + result.confidence + ")");
      }
      ```

      ```php PHP
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Classification implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $category;
          public float $confidence;
          public array $tags;
          public string $sentiment;
      }

      $feedbackText = "Great product, fast shipping!";

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => "Classify this feedback: {$feedbackText}"]
          ],
          model: 'claude-opus-5-5',
          outputConfig: ['format' => Classification::class],
      );

      $result = $message->parsedOutput();
      if ($result instanceof Classification) {
          echo "{$result->category} ({$result->confidence}): {$result->sentiment}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class Classification < Anthropic::BaseModel
        required :category, String
        required :confidence, Float
        required :tags, Anthropic::ArrayOf[String]
        required :sentiment, String
      end

      feedback_text = "Great product, fast shipping!"

      message = client.messages.create(
        model: "claude-opus-5-5",
        max_tokens: 1024,
        output_config: {format: Classification},
        messages: [
          {role: "user", content: "Classify this feedback: #{feedback_text}"}
        ]
      )
      puts message.parsed_output
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="API response formatting">
    Generate API-ready responses:

    <CodeGroup>
      ```bash cURL
      curl https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 1024,
          "messages": [
            {
              "role": "user",
              "content": "Process this request: ..."
            }
          ],
          "output_config": {
            "format": {
              "type": "json_schema",
              "schema": {
                "type": "object",
                "properties": {
                  "status": {"type": "string"},
                  "data": {"type": "object", "additionalProperties": false},
                  "errors": {
                    "type": "array",
                    "items": {"type": "object", "additionalProperties": false}
                  },
                  "metadata": {"type": "object", "additionalProperties": false}
                },
                "required": ["status", "data", "metadata"],
                "additionalProperties": false
              }
            }
          }
        }'
      ```

      ```bash CLI
      ant messages create \
        --transform 'content.#(type=="text").text' \
        --raw-output <<'YAML'
      model: claude-opus-5-5
      max_tokens: 1024
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              status:
                type: string
              data:
                type: object
                additionalProperties: false
              errors:
                type: array
                items:
                  type: object
                  additionalProperties: false
              metadata:
                type: object
                additionalProperties: false
            required:
              - status
              - data
              - metadata
            additionalProperties: false
      messages:
        - role: user
          content: "Process this request: ..."
      YAML
      ```

      ```python Python
      from pydantic import BaseModel

      client = Anthropic()


      class APIResponse(BaseModel):
          status: str
          data: dict
          errors: list[dict] | None
          metadata: dict


      response = client.messages.parse(
          model="claude-opus-5-5",
          max_tokens=1024,
          output_format=APIResponse,
          messages=[{"role": "user", "content": "Process this request: ..."}],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const APIResponseSchema = z.object({
        status: z.string(),
        data: z.record(z.string(), z.any()),
        errors: z.array(z.record(z.string(), z.any())).optional(),
        metadata: z.record(z.string(), z.any())
      });

      const response = await client.messages.parse({
        model: "claude-opus-5-5",
        max_tokens: 1024,
        output_config: { format: zodOutputFormat(APIResponseSchema) },
        messages: [{ role: "user", content: "Process this request..." }]
      });

      console.log(response.parsed_output);
      ```

      ```csharp C#
      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Process this request: ..." }],
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          status = new { type = "string" },
                          data = new { type = "object", additionalProperties = false },
                          errors = new
                          {
                              type = "array",
                              items = new { type = "object", additionalProperties = false },
                          },
                          metadata = new { type = "object", additionalProperties = false },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "status", "data", "metadata" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus5_5,
      	MaxTokens: 1024,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: map[string]any{
      				"type":                 "object",
      				"additionalProperties": false,
      				"properties": map[string]any{
      					"status": map[string]any{
      						"type": "string",
      					},
      					"data": map[string]any{
      						"type":                 "object",
      						"additionalProperties": false,
      					},
      					"errors": map[string]any{
      						"type": "array",
      						"items": map[string]any{
      							"type":                 "object",
      							"additionalProperties": false,
      						},
      					},
      					"metadata": map[string]any{
      						"type":                 "object",
      						"additionalProperties": false,
      					},
      				},
      				"required": []string{"status", "data", "metadata"},
      			},
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("Process this request: ...")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		fmt.Println(variant.Text)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class APIData {
          @JsonProperty("message")
          public String message;

          @JsonProperty("resource_id")
          public String resourceId;
      }

      static class APIError {
          @JsonProperty("code")
          public String code;

          @JsonProperty("message")
          public String message;
      }

      static class APIMetadata {
          @JsonProperty("request_id")
          public String requestId;

          @JsonProperty("timestamp")
          public String timestamp;
      }

      static class APIResponse {
          @JsonProperty("status")
          public String status;

          @JsonProperty("data")
          public APIData data;

          @JsonProperty("errors")
          public List<APIError> errors;

          @JsonProperty("metadata")
          public APIMetadata metadata;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          StructuredMessageCreateParams<APIResponse> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024L)
              .outputConfig(APIResponse.class)
              .addUserMessage("Process this request: ...")
              .build();

          StructuredMessage<APIResponse> response = client.messages().create(params);
          APIResponse result = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(result.status);
      }
      ```

      ```php PHP
      use Anthropic\Lib\Attributes\Constrained;
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Payload implements StructuredOutputModel { use StructuredOutputModelTrait; public string $message; }

      class APIError implements StructuredOutputModel { use StructuredOutputModelTrait; public string $code; public string $detail; }

      class Metadata implements StructuredOutputModel { use StructuredOutputModelTrait; public string $request_id; }

      class APIResponse implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $status;
          public Payload $data;
          #[Constrained(itemClass: APIError::class)]
          public ?array $errors;
          public Metadata $metadata;
      }

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Process this request: ...']
          ],
          model: 'claude-opus-5-5',
          outputConfig: ['format' => APIResponse::class],
      );

      $result = $message->parsedOutput();
      if ($result instanceof APIResponse) {
          echo "{$result->status}: {$result->data->message}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class Payload < Anthropic::BaseModel
        required :message, String
      end

      class APIError < Anthropic::BaseModel
        required :code, String
        required :detail, String
      end

      class Metadata < Anthropic::BaseModel
        required :request_id, String
      end

      class APIResponse < Anthropic::BaseModel
        required :status, String
        required :data, Payload
        optional :errors, Anthropic::ArrayOf[APIError]
        required :metadata, Metadata
      end

      message = client.messages.create(
        model: "claude-opus-5-5",
        max_tokens: 1024,
        output_config: {format: APIResponse},
        messages: [
          {role: "user", content: "Process this request: ..."}
        ]
      )
      puts message.parsed_output
      ```
    </CodeGroup>
  </Accordion>
</AccordionGroup>

## Strict tool use

To enforce JSON Schema compliance on tool inputs with grammar-constrained sampling, see [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use).

### Using both features together

JSON outputs and strict tool use solve different problems and work together:

* **JSON outputs** control Claude's response format (what Claude says)
* **Strict tool use** validates tool parameters (how Claude calls your functions)

When combined, Claude can call tools with guaranteed-valid parameters AND return structured JSON responses. This is useful for agentic workflows where you need both reliable tool calls and structured final outputs.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": "Help me plan a trip to Paris departing May 15, 2026"
        }
      ],
      "output_config": {
        "format": {
          "type": "json_schema",
          "schema": {
            "type": "object",
            "properties": {
              "summary": {"type": "string"},
              "next_steps": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["summary", "next_steps"],
            "additionalProperties": false
          }
        }
      },
      "tools": [
        {
          "name": "search_flights",
          "strict": true,
          "input_schema": {
            "type": "object",
            "properties": {
              "destination": {"type": "string"},
              "date": {"type": "string", "format": "date"}
            },
            "required": ["destination", "date"],
            "additionalProperties": false
          }
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  messages:
    - role: user
      content: Help me plan a trip to Paris departing May 15, 2026
  # JSON outputs: structured response format
  output_config:
    format:
      type: json_schema
      schema:
        type: object
        properties:
          summary:
            type: string
          next_steps:
            type: array
            items:
              type: string
        required: [summary, next_steps]
        additionalProperties: false
  # Strict tool use: guaranteed tool parameters
  tools:
    - name: search_flights
      strict: true
      input_schema:
        type: object
        properties:
          destination:
            type: string
          date:
            type: string
            format: date
        required: [destination, date]
        additionalProperties: false
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Help me plan a trip to Paris departing May 15, 2026",
          }
      ],
      # JSON outputs: structured response format
      output_config={
          "format": {
              "type": "json_schema",
              "schema": {
                  "type": "object",
                  "properties": {
                      "summary": {"type": "string"},
                      "next_steps": {"type": "array", "items": {"type": "string"}},
                  },
                  "required": ["summary", "next_steps"],
                  "additionalProperties": False,
              },
          }
      },
      # Strict tool use: guaranteed tool parameters
      tools=[
          {
              "name": "search_flights",
              "strict": True,
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "destination": {"type": "string"},
                      "date": {"type": "string", "format": "date"},
                  },
                  "required": ["destination", "date"],
                  "additionalProperties": False,
              },
          }
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Help me plan a trip to Paris departing May 15, 2026" }],
    // JSON outputs: structured response format
    output_config: {
      format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            summary: { type: "string" },
            next_steps: { type: "array", items: { type: "string" } }
          },
          required: ["summary", "next_steps"],
          additionalProperties: false
        }
      }
    },
    // Strict tool use: guaranteed tool parameters
    tools: [
      {
        name: "search_flights",
        description: "Search for available flights to a destination on a specific date",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            destination: { type: "string" },
            date: { type: "string", format: "date" }
          },
          required: ["destination", "date"],
          additionalProperties: false
        }
      }
    ]
  });

  // Claude may call the tool first (tool_use) or respond with JSON (text)
  console.log("Stop reason:", response.stop_reason);
  for (const block of response.content) {
    switch (block.type) {
      case "tool_use":
        console.log(`Tool call: ${block.name}(${JSON.stringify(block.input)})`);
        break;
      case "text":
        console.log("Response:", block.text);
        break;
    }
  }
  ```

  ```csharp C#
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Help me plan a trip to Paris departing May 15, 2026" }],
      // JSON outputs: structured response format
      OutputConfig = new OutputConfig
      {
          Format = new JsonOutputFormat
          {
              Schema = new Dictionary<string, JsonElement>
              {
                  ["type"] = JsonSerializer.SerializeToElement("object"),
                  ["properties"] = JsonSerializer.SerializeToElement(new
                  {
                      summary = new { type = "string" },
                      next_steps = new { type = "array", items = new { type = "string" } },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "summary", "next_steps" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              },
          },
      },
      // Strict tool use: guaranteed tool parameters
      Tools =
      [
          new Tool
          {
              Name = "search_flights",
              Strict = true,
              InputSchema = new InputSchema(new Dictionary<string, JsonElement>
              {
                  ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                  {
                      ["destination"] = new { type = "string" },
                      ["date"] = new { type = "string", format = "date" },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "destination", "date" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              }),
          }
      ],
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Help me plan a trip to Paris departing May 15, 2026")),
  	},
  	// JSON outputs: structured response format
  	OutputConfig: anthropic.OutputConfigParam{
  		Format: anthropic.JSONOutputFormatParam{
  			Schema: map[string]any{
  				"type":                 "object",
  				"additionalProperties": false,
  				"properties": map[string]any{
  					"summary":    map[string]any{"type": "string"},
  					"next_steps": map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
  				},
  				"required": []string{"summary", "next_steps"},
  			},
  		},
  	},
  	// Strict tool use: guaranteed tool parameters
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:   "search_flights",
  			Strict: anthropic.Bool(true),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"destination": map[string]any{"type": "string"},
  					"date":        map[string]any{"type": "string", "format": "date"},
  				},
  				Required: []string{"destination", "date"},
  				ExtraFields: map[string]any{
  					"additionalProperties": false,
  				},
  			}}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // JSON outputs: structured response format
  JsonOutputFormat.Schema outputSchema = JsonOutputFormat.Schema.builder()
      .putAdditionalProperty("type", JsonValue.from("object"))
      .putAdditionalProperty("properties", JsonValue.from(Map.of(
          "summary", Map.of("type", "string"),
          "next_steps", Map.of("type", "array", "items", Map.of("type", "string"))
      )))
      .putAdditionalProperty("required", JsonValue.from(List.of("summary", "next_steps")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  // Strict tool use: guaranteed tool parameters
  InputSchema toolSchema = InputSchema.builder()
      .properties(JsonValue.from(Map.of(
          "destination", Map.of("type", "string"),
          "date", Map.of("type", "string", "format", "date")
      )))
      .putAdditionalProperty("required", JsonValue.from(List.of("destination", "date")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024L)
      .addUserMessage("Help me plan a trip to Paris departing May 15, 2026")
      .outputConfig(OutputConfig.builder()
          .format(JsonOutputFormat.builder().schema(outputSchema).build())
          .build())
      .addTool(Tool.builder()
          .name("search_flights")
          .description("Search for available flights to a destination on a specific date")
          .strict(true)
          .inputSchema(toolSchema)
          .build())
      .build();

  Message response = client.messages().create(params);
  IO.println(response);
  ```

  ```php PHP
  use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
  use Anthropic\Lib\Contracts\StructuredOutputModel;
  use Anthropic\Messages\ToolUseBlock;

  $client = new Client();

  class TripPlan implements StructuredOutputModel
  {
      use StructuredOutputModelTrait;

      public string $summary;
      public array $next_steps;
  }

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Help me plan a trip to Paris departing May 15, 2026']
      ],
      model: 'claude-opus-5-5',
      // JSON outputs: structured response format
      outputConfig: ['format' => TripPlan::class],
      // Strict tool use: guaranteed tool parameters
      tools: [
          [
              'name' => 'search_flights',
              'strict' => true,
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'destination' => ['type' => 'string'],
                      'date' => ['type' => 'string', 'format' => 'date']
                  ],
                  'required' => ['destination', 'date'],
                  'additionalProperties' => false
              ]
          ]
      ],
  );

  // Claude may call the tool first (tool_use) or respond with JSON (text)
  $plan = $message->parsedOutput();
  if ($plan instanceof TripPlan) {
      echo $plan->summary, "\n";
  } elseif ($toolUse = array_find($message->content, fn($block) => $block instanceof ToolUseBlock)) {
      echo "Tool call: {$toolUse->name}(", json_encode($toolUse->input), ")\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [
      {role: "user", content: "Help me plan a trip to Paris departing May 15, 2026"}
    ],
    # JSON outputs: structured response format
    output_config: {
      format: {
        type: :json_schema,
        schema: {
          type: "object",
          properties: {
            summary: {type: "string"},
            next_steps: {type: "array", items: {type: "string"}}
          },
          required: ["summary", "next_steps"],
          additionalProperties: false
        }
      }
    },
    # Strict tool use: guaranteed tool parameters
    tools: [
      {
        name: "search_flights",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            destination: {type: "string"},
            date: {type: "string", format: "date"}
          },
          required: ["destination", "date"],
          additionalProperties: false
        }
      }
    ]
  )
  puts message
  ```
</CodeGroup>

## Important considerations

### Grammar compilation and caching

Structured outputs use constrained sampling with compiled grammar artifacts. This introduces some performance characteristics to be aware of:

* **First request latency:** The first time you use a specific schema, there is additional latency while the grammar compiles

* **Automatic caching:** Compiled grammars are cached for 24 hours from last use, making subsequent requests much faster

* **Cache invalidation:** The cache is invalidated if you change:

  * The JSON schema structure
  * The set of tools in your request (when using both structured outputs and tool use)
  * Changing only `name` or `description` fields does not invalidate the cache

### Prompt modification and token costs

When using structured outputs, Claude automatically receives an additional system prompt explaining the expected output format. This means:

* Your input token count is slightly higher
* The injected prompt costs you tokens like any other system prompt
* Changing the `output_config.format` parameter will invalidate any [prompt cache](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) for that conversation thread

### JSON Schema limitations

Structured outputs support standard JSON Schema with some limitations. Both JSON outputs and strict tool use share these limitations.

<Accordion title="Supported features">
  * All basic types: object, array, string, integer, number, boolean, null
  * `enum` (strings, numbers, bools, or nulls only - no complex types). For a capitalization caveat, see [Invalid outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#invalid-outputs).
  * `const`
  * `anyOf` and `allOf` (with limitations - `allOf` with `$ref` not supported)
  * `$ref`, `$def`, and `definitions` (external `$ref` not supported)
  * `default` property for all supported types
  * `required` and `additionalProperties` (must be set to `false` for objects)
  * String formats: `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`
  * Array `minItems` (only values 0 and 1 supported)
</Accordion>

<Accordion title="Not supported">
  * Recursive schemas
  * Complex types within enums
  * External `$ref` (for example, `'$ref': 'http://...'`)
  * Numerical constraints (such as `minimum`, `maximum`, `multipleOf`)
  * String constraints (`minLength`, `maxLength`)
  * Array constraints beyond `minItems` of 0 or 1
  * `additionalProperties` set to anything other than `false`

  If you use an unsupported feature, you'll receive a 400 error with details.
</Accordion>

<Accordion title="Pattern support (regex)">
  **Supported regex features:**

  * Full matching (`^...$`) and partial matching
  * Quantifiers: `*`, `+`, `?`, simple `{n,m}` cases
  * Character classes: `[]`, `.`, `\d`, `\w`, `\s`
  * Groups: `(...)`

  **NOT supported:**

  * Backreferences to groups (for example, `\1`, `\2`)
  * Lookahead/lookbehind assertions (for example, `(?=...)`, `(?!...)`)
  * Word boundaries: `\b`, `\B`
  * Complex `{n,m}` quantifiers with large ranges

  Simple regex patterns work well. Complex patterns may result in 400 errors.
</Accordion>

<Tip>
  SDK helpers can transform schemas with [constraints not supported by the API](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations). See [How SDK transformation works](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#how-sdk-transformation-works).
</Tip>

### Property ordering

When using structured outputs, properties in objects maintain their defined ordering from your schema, with one important caveat: **required properties appear first, followed by optional properties**.

For example, given this schema:

```json
{
  "type": "object",
  "properties": {
    "notes": { "type": "string" },
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email"],
  "additionalProperties": false
}
```

The output will order properties as:

1. `name` (required, in schema order)
2. `email` (required, in schema order)
3. `notes` (optional, in schema order)
4. `age` (optional, in schema order)

This means the output might look like:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "notes": "Interested in enterprise plan",
  "age": 35
}
```

If property order in the output is important to your application, mark all properties as required, or account for this reordering in your parsing logic.

### Invalid outputs

While structured outputs guarantee schema compliance in most cases, there are scenarios where the output may not match your schema:

**Refusals** (`stop_reason: "refusal"`)

Claude maintains its safety and helpfulness properties even when using structured outputs. If Claude refuses a request for safety reasons:

* The response has `stop_reason: "refusal"`
* You'll receive a 200 status code
* You'll be billed for the tokens generated
* The output may not match your schema because the refusal message takes precedence over schema constraints

A property that asks for the model's thinking or step-by-step reasoning may lead to a `reasoning_extraction` refusal. Ask for a short explanation instead. See [Keep reasoning in thinking blocks](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks).

**Token limit reached** (`stop_reason: "max_tokens"`)

If the response is cut off due to reaching the `max_tokens` limit:

* The response has `stop_reason: "max_tokens"`
* The output may be incomplete and not match your schema
* Retry with a higher `max_tokens` value to get the complete structured output

**Enum value casing**

Structured outputs don't guarantee the capitalization of string `enum` and `const` values: Claude may return a value that differs from your schema only in capitalization, typically in the first letter of a word following a space. For example, given this schema:

```json
{
  "type": "string",
  "enum": ["Conversation Topic 1", "Conversation Topic 2", "Conversation topic 3"]
}
```

The output may contain `"Conversation Topic 3"` (capital "T") even though that exact value isn't in the enum. The response completes normally, with no error and no special `stop_reason`. This applies to both JSON outputs and strict tool use. Compare enum values case-insensitively, and avoid enum values that differ only in capitalization.

### Schema complexity limits

Structured outputs work by compiling your JSON schemas into a grammar that constrains Claude's output. More complex schemas produce larger grammars that take longer to compile. To protect against excessive compilation times, the API enforces several complexity limits.

#### Explicit limits

The following limits apply to all requests with `output_config.format` or `strict: true`:

| Limit                       | Value | Description                                                                                                                                                                                              |
| --------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strict tools per request    | 20    | Maximum number of tools with `strict: true`. Non-strict tools don't count toward this limit.                                                                                                             |
| Optional parameters         | 24    | Total optional parameters across all strict tool schemas and JSON output schemas. Each parameter not listed in `required` counts toward this limit.                                                      |
| Parameters with union types | 16    | Total parameters that use `anyOf` or type arrays (for example, `"type": ["string", "null"]`) across all strict schemas. These are especially expensive because they create exponential compilation cost. |

<Note>
  These limits apply to the combined total across all strict schemas in a single request. For example, if you have 4 strict tools with 6 optional parameters each, you'll reach the 24-parameter limit even though no single tool seems complex.
</Note>

#### Additional internal limits

Beyond the explicit limits in the preceding table, there are additional internal limits on the compiled grammar size. These limits exist because schema complexity doesn't reduce to a single dimension: features like optional parameters, union types, nested objects, and number of tools interact with each other in ways that can make the compiled grammar disproportionately large.

When these limits are exceeded, you'll receive a 400 error with the message "Schema is too complex for compilation." These errors mean the combined complexity of your schemas exceeds what can be efficiently compiled, even if each individual limit in the preceding table is satisfied. As a final stop-gap, the API also enforces a **compilation timeout of 180 seconds**. Schemas that pass all explicit checks but produce very large compiled grammars may hit this timeout.

#### Tips for reducing schema complexity

If you're hitting complexity limits, try these strategies in order:

1. **Mark only critical tools as strict.** If you have many tools, reserve it for tools where schema violations cause real problems, and rely on Claude's natural adherence for simpler tools.

2. **Reduce optional parameters.** Make parameters `required` where possible. Each optional parameter roughly doubles a portion of the grammar's state space. If a parameter always has a reasonable default, consider making it required and having Claude provide that default explicitly.

3. **Simplify nested structures.** Deeply nested objects with optional fields compound the complexity. Flatten structures where possible.

4. **Split into multiple requests.** If you have many strict tools, consider splitting them across separate requests or sub-agents.

For persistent issues with valid schemas, [contact support](https://support.claude.com/en/articles/9015913-how-to-get-support) with your schema definition.

## Migrating from the beta

The `output_format` parameter has moved to `output_config.format`, and beta headers are no longer required. The `output_format` parameter is deprecated and will be removed in the future. To use it anyway, add the `structured-outputs-2025-11-13` beta header. Without it, the API returns a 400 error.

The Python SDK (v1.0 and later) does not accept `output_format={...}` on `client.beta.messages.create()` or `count_tokens()` and raises a `TypeError`. Use `output_config` instead. See [Using a raw JSON schema](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#using-a-raw-json-schema) for the updated API shape.

## Data retention

Prompts and responses are processed with ZDR when using structured outputs. However, the JSON schema itself is temporarily cached for up to 24 hours since last use for optimization purposes. No prompt or response data is retained beyond the API response.

Structured outputs are HIPAA eligible, but **PHI must not be included in JSON schema definitions**. The API compiles JSON schemas into grammars that are cached separately from message content, and these cached schemas do not receive the same PHI protections as prompts and responses. Do not include PHI in schema property names, `enum` values, `const` values, or `pattern` regular expressions. PHI should only appear in message content (prompts and responses), where it is protected under HIPAA safeguards.

For ZDR and HIPAA eligibility across all features, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).

## Feature compatibility

**Works with:**

* **[Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing):** Process structured outputs at scale with 50% discount
* **[Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting):** Count tokens without compilation
* **[Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming):** Stream structured outputs like normal responses
* **[Combined usage](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#using-both-features-together):** Use JSON outputs (`output_config.format`) and strict tool use (`strict: true`) together in the same request

**Incompatible with:**

* **[Citations](https://platform.claude.com/docs/en/build-with-claude/citations):** Citations require interleaving citation blocks with text, which conflicts with strict JSON schema constraints. Returns 400 error if citations enabled with `output_config.format`.
* **Message Prefilling:** Incompatible with JSON outputs

<Tip>
  **Grammar scope:** Grammars apply only to Claude's direct output, not to tool use calls, tool results, or thinking tags (when using [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)). Grammar state resets between sections, allowing Claude to think freely while still producing structured output in the final response.
</Tip>

## Next steps

<CardGroup cols={2}>
  <Card title="Citations" icon="book-bookmark" href="https://platform.claude.com/docs/en/build-with-claude/citations">
    Have Claude cite its sources when answering questions about provided documents.
  </Card>

  <Card title="Strict tool use" icon="check" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use">
    Enforce JSON Schema compliance on Claude's tool inputs with grammar-constrained sampling.
  </Card>

  <Card title="Tool use with Claude" icon="wrench" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview">
    Connect Claude to external tools and APIs. Learn where tools execute and how the agentic loop works.
  </Card>

  <Card title="Pricing" icon="calculator" href="https://platform.claude.com/docs/en/about-claude/pricing">
    Learn about Anthropic's pricing structure for models and features.
  </Card>
</CardGroup>