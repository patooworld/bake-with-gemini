import {HumanMessage} from '@langchain/core/messages';
import {ChatGoogleGenerativeAI} from '@langchain/google-genai';
import {HarmBlockThreshold, HarmCategory} from '@google/generative-ai';
import Base64 from 'base64-js';
import MarkdownIt from 'markdown-it';
import {maybeShowApiKeyBanner} from './gemini-api-banner';
import './style.css';

// 🔥 SET `GOOGLE_API_KEY` IN YOUR .env FILE! 🔥
// 🔥 GET YOUR GEMINI API KEY AT 🔥
// 🔥 https://g.co/ai/idxGetGeminiKey 🔥

const form = document.querySelector('form');
const promptInput = document.querySelector('input[name="prompt"]');
const output = document.querySelector('.output');

form.onsubmit = async ev => {
  ev.preventDefault();
  output.textContent = 'Generating...';

  try {
    // Load the image as a base64 string
    const imageUrl = form.elements.namedItem('chosen-image').value;
    const imageBase64 = await fetch(imageUrl)
      .then(r => r.arrayBuffer())
      .then(a => Base64.fromByteArray(new Uint8Array(a)));

    const contents = [
      new HumanMessage({
        content: [
          {
            type: 'text',
            text: promptInput.value,
          },
          {
            type: 'image_url',
            image_url: `data:image/png;base64,${imageBase64}`,
          },
        ],
      }),
    ];

    // Call the multimodal model, and get a stream of results
    const vision = new ChatGoogleGenerativeAI({
      modelName: 'gemini-1.5-flash-vision', // Update to the new model
  // ... other settings ...

    });

    // Multi-modal streaming
    const streamRes = await vision.stream(contents);

    // Read from the stream and interpret the output as markdown
    const buffer = [];
    const md = new MarkdownIt();

    for await (const chunk of streamRes) {
      buffer.push(chunk.content);
      output.innerHTML = md.render(buffer.join(''));
    }
  } catch (e) {
    output.innerHTML += '<hr>' + e;
  }
};

// You can delete this once you've filled out an API key
maybeShowApiKeyBanner(process.env.GOOGLE_API_KEY, `enter it in your <code>.env</code> file.`);


const {VertexAI} = require('@google-cloud/vertexai');

// Initialize Vertex with your Cloud project and location
const vertex_ai = new VertexAI({project: 'elite-flow-386908', location: 'us-central1'});
const model = 'gemini-1.5-pro-002';

// Instantiate the models
const generativeModel = vertex_ai.preview.getGenerativeModel({
  model: model,
  generationConfig: {
    'maxOutputTokens': 1024,
    'temperature': 0.2,
    'topP': 0.95,
  },
  safetySettings: [
    {
      'category': 'HARM_CATEGORY_HATE_SPEECH',
      'threshold': 'OFF',
    },
    {
      'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
      'threshold': 'OFF',
    },
    {
      'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
      'threshold': 'OFF',
    },
    {
      'category': 'HARM_CATEGORY_HARASSMENT',
      'threshold': 'OFF',
    }
  ],
  systemInstruction: {
    parts: [textsi_1]
  },
});

const textsi_1 = {text: `You are a chatbot for the county\\\'s performing and fine arts program. You help students decide what course they will take during the summer. Please follow these guidelines.

1. DO NOT HALLUCINATE.
2. Use only English.
3. Output a short letter to the student with your recommendation.
4. Use a fun, motivational tone.
5. Congratulate the student, whether it is for continuing with a certain discipline or trying something new.
6. Empower them about developing as an artist, making them feel good about their summer plans.
7. Include a greeting and sign-off that lean into the fun and motivational persona.
8. Do not use the internet.
9. Follow each step, one at a time.

Step 1: Decide which art the student likes from 2 choices: \"Performing Arts\" or \"Fine Arts.\"
1a. If they answer \"Performing Arts,\" move to step 2.
1b. If they answer \"Fine Arts,\" move to step 3.

Step 2:
2a. In this section, if the student has taken Theater 1A, make a recommendation that they enroll in Theater 2A.
2b. If the student has taken Theater 2A, make a recommendation to enroll in Theater 3B.

Step 3:
3a. Decide which option the student likes the most: Photography, Sculpting, or Painting
3b. If they are interested in \"Photography,\" move to step 4.
3c. If they are interested in \"Sculpting,\" move to step 5.
3d. If they are interested in \"Painting,\" move to step 6.

Step 4: For \"Photography,\" suggest the course Photography 1A: Stills.

Step 5. For \"Sculpting,\" suggest the course Sculpture Garden 1A.

Step 6: For \"Painting,\" suggest Self-Portrait Oils 1A.`};

async function generateContent() {
  const req = {
    contents: [
      {role: 'user', parts: [{text: `I am interested in Performing Arts. I have taken Theater 1A.`}]}
    ],
  };

  const streamingResp = await generativeModel.generateContentStream(req);

  for await (const item of streamingResp.stream) {
    process.stdout.write('stream chunk: ' + JSON.stringify(item) + '\n');
  }

  process.stdout.write('aggregated response: ' + JSON.stringify(await streamingResp.response));
}

generateContent();