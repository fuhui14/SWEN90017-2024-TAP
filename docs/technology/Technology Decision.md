## Technology decisions Records

- language: 
    + Frontend: Javascript
    + Backend : python 3.12.3

- Framework: 
    + Frontend: React
    + Backend : Django

- Library: 
    + Transcription: OpenAI Whisper
    + Speaker Identifier: 

## Frontend Framework

| Framework | Introduction | Version | Pros | Cons | Will Use |
| :-------: | :----------: | :-----: | :--: | :--: | :------: |
|  React  | A JavaScript library for building user interfaces. React is component-based, making it easy to create interactive UIs. | [v18.3.1](https://react.dev/versions) | - **Component-Based Architecture**: Perfect for building modular and reusable components, which is ideal for integrating dynamic transcription results and user interfaces. <br> - **Seamless Django Integration**: React can be easily paired with Django to create a robust full-stack application, allowing Django to handle the backend logic and React to manage the frontend UI. <br> - **Optimized for Real-Time Updates**: React’s virtual DOM efficiently handles frequent UI updates, which is crucial when displaying real-time transcription and speaker identification results from OpenAI Whisper. <br> - **Strong Ecosystem**: A vast ecosystem of libraries and tools makes it easier to extend functionalities, such as state management and routing, enhancing the overall application experience. | - Requires learning JSX, which can be confusing for new users. <br> - Often requires additional libraries for state management and routing. |   x   |
|  Angular  | A platform for building mobile and desktop web applications. Angular provides a full framework with built-in features. | [v18.0.0](https://angular.dev/reference/releases) | - **Comprehensive**: Offers a full-fledged MVC framework.  <br> - Strong type-checking with TypeScript. <br> - Two-way data binding simplifies UI updates. | - Steeper learning curve. <br> - Can be heavy for simple applications. |       |
|  Vue.js  | A progressive JavaScript framework for building user interfaces, focusing on simplicity and flexibility. | [v3.4.38](https://github.com/vuejs/core/blob/main/CHANGELOG.md) | - **Simplicity**: Easy to integrate and get started. <br> - Flexible and incrementally adoptable. <br> - Strong community and ecosystem. | - Smaller community than React and Angular. <br> - Somewhat less opinionated, leading to different coding practices. |       |
|  Svelte  | A radical new approach to building user interfaces, compiling components to highly efficient imperative code. | [v4.2.19](https://github.com/sveltejs/svelte/blob/svelte-4/packages/svelte/CHANGELOG.md) | - **Performance**: Compiles to highly optimized vanilla JS, eliminating the need for a virtual DOM. <br> - Simple and clean syntax. <br> - Reduces boilerplate code. | - Smaller community and ecosystem compared to React, Angular, or Vue. <br> - Limited tooling and ecosystem support. |       |
|  Ember.js	  | A framework for building ambitious web applications. Ember follows a convention-over-configuration philosophy. | [v5.11.0](https://github.com/emberjs/ember.js/releases) | - **Convention-Over-Configuration**: Reduces decision fatigue by providing strong conventions. <br> - Comprehensive tooling and strong community support. | - Less flexible and heavier than other frameworks. <br> - Slower learning curve due to its comprehensive nature. |       |

## Backend Framework

| Framework | Introduction | Version | Pros | Cons | Will Use |
| :-------: | :----------: | :-----: | :--: | :--: | :------: |
|  Django   | A high-level Python web framework that encourages rapid development and clean, pragmatic design. | | - **Integration-Friendly**: Django's robust ecosystem allows seamless integration with AI libraries like OpenAI Whisper. <br> - Batteries-included: Comes with built-in features for admin interface, authentication, ORM, etc. <br> - Strong community support and extensive documentation. | - Monolithic: Can be heavyweight for small projects. <br> - Steeper learning curve due to its comprehensive nature. |    x   |
|   Flask   | A lightweight WSGI web application framework in Python.                      | | - **Flexibility**: Easy to integrate with OpenAI Whisper and other AI libraries. <br> - Minimalistic: Provides simplicity and ease of use. <br> - Modular and easy to extend. | - Requires additional libraries for full-stack capabilities. <br> - Less opinionated, which can lead to inconsistencies in large teams. |        |
|  Tornado  | A Python web framework and asynchronous networking library, originally developed at FriendFeed. | | - **Performance**: Non-blocking and asynchronous, making it suitable for handling real-time audio processing with OpenAI Whisper. <br> - Good for applications needing high concurrency. | - Steeper learning curve for asynchronous programming. <br> - Smaller ecosystem compared to Django or Flask. |        |
|  Pyramid  | A flexible Python web framework suitable for both small and large applications. | | - **Scalability**: Can scale with the project size, making it adaptable to evolving needs. <br> - Allows easy integration with different components, including AI libraries like Whisper. | - Less out-of-the-box features compared to Django. <br> - Requires more configuration, which can slow down initial development. |        |
| CherryPy  | A minimalist Python web framework, object-oriented and designed for rapid development. | | - **Lightweight**: Minimalist design allows direct integration with Whisper without unnecessary overhead. <br> - Fast and easy to deploy. | - Lacks built-in features, requiring manual integration of many components. <br> - Smaller community and less documentation. |        |

## Different Library


|    Library     | Introduction | Version | Pros | Cons | Will Use |
| :------------: | :----------: | :-----: |:--: | :--: | :------: |
| OpenAI Whisper |  OpenAI Whisper is a large-scale speech recognition model designed specifically for multi-language and multi-task speech recognition and translation tasks. It uses 680,000 hours of diverse audio data for training, can accurately transcribe and translate speech in a variety of contexts and languages, and can perform well on new datasets without fine-tuning. |  [v20231117](https://github.com/openai/whisper/releases/tag/v20231117) |  - Multi-language support: supports multiple languages ​​and tasks, and is highly adaptable. <br> - High robustness: has good generalization ability in noisy environments and datasets with different distributions. <br> - No fine-tuning required: can achieve excellent performance in zero-shot settings.   |  - Data dependence: Relying on a large amount of weakly supervised data, which may contain noise and annotation errors. <br> - Resource requirements: A large amount of computing resources are required during training and inference, especially when processing large-scale data.    |    x    |
| pyannote.audio | pyannote.audio is an open-source toolkit written in Python for speaker diarization. Based on PyTorch machine learning framework, it comes with state-of-the-art pretrained models and pipelines, that can be further finetuned to your own data for even better performance. | [version3.3.1](https://github.com/pyannote/pyannote-audio/releases/tag/3.3.1) | - Provides pre-trained models, easy to get started. <br> - Supports a variety of speech tasks. | - Requires higher computing resources, especially when processing long audio. <br> - Not easy to use. |          |
|  speechbrain   | SpeechBrain is an open-source PyTorch toolkit that accelerates Conversational AI development, i.e., the technology behind speech assistants, chatbots, and large language models. <br> It is crafted for fast and easy creation of advanced technologies for Speech and Text Processing. | [v1.0](https://github.com/speechbrain/speechbrain/releases/tag/v1.0.0) | - Supports multi-tasking and modular design. <br> - Has a large number of pre-trained models and rich community support. | - Requires some background knowledge in machine learning. <br> - Configuration and optimization may be complicated. |          |
|  Resemblyzer   | Resemblyzer allows you to derive a high-level representation of a voice through a deep learning model (referred to as the voice encoder). Given an audio file of speech, it creates a summary vector of 256 values that summarizes the characteristics of the voice spoken. |    [git](https://github.com/resemble-ai/Resemblyzer)     | - Can quickly generate speaker embeddings. <br> - Easy to integrate into other speech processing pipelines. | - Limited processing efficiency for long audio.     |          |


## Testing Tools

| **Component** | **Testing Framework** | **Purpose** |
|--------------|----------------------|------------|
| **Frontend** | Jest | Test JavaScript logic & React components |
| **Backend** | Django `unittest` | Test Django models and core functions |
