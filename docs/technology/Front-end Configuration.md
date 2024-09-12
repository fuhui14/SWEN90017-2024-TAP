# Front-End Configuration Document

## Overview

This document outlines the configuration and setup for the front-end environment of the **Transcription Aid Platform(TAP)**. It includes details on the necessary tools, libraries, and environment settings required for development, testing, and deployment.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Environment Setup](#environment-setup)
   - Prerequisites
   - Installation
3. [Development Configuration](#development-configuration)
   - Package Manager
   - Project Scripts
   - Environment Variables
4. [Build Configuration](#build-configuration)
   - Webpack Configuration
   - Babel Configuration
5. [Testing Configuration](#testing-configuration)
   - Unit Test
   - Integration Test
   - Acceptance Test
6. [Styling and Theming](#styling-and-theming)
   - CSS Preprocessor
   - Theme Configuration
7. [Version Control](#version-control)
8. [Deployment Configuration](#deployment-configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Project Structure

Outline the structure of your project, including key directories and files.

```plaintext
|-- src/
|   |-- assets/
|   |-- components/
|   |-- pages/
|   |-- services/
|   |-- styles/
|   |-- App.js
|   |-- index.js
|-- public/
|-- .env
|-- package.json
|-- webpack.config.js
|-- README.md

```
## Environment Setup

### Prerequisites
Ensure the following are installed on your machine:
- npm or yarn: For managing dependencies
- Git: Version control system

### Installation
Clone the repository and install the necessary dependencies:
```bash
git clone https://github.com/fuhui14/SWEN90017-2024-TAP.git
cd SWEN90017-2024-TAP
npm install
```
## Development Configuration

### Package Manager
Specify the package manager being used (npm or yarn) and any important commands:
- Install Dependencies: `npm install`
- Start Development Server: `npm start`
- Build for Production: `npm run build`

### Project Scripts
List custom scripts defined in package.json:
```json
"scripts": {
  "start": "webpack serve --config webpack.dev.js",
  "build": "webpack --config webpack.prod.js",
  "test": "jest",
  "lint": "eslint ./src"
}
```

### Environment Variables
Describe how to set up environment variables using a .env file.
```plaintext
REACT_APP_API_URL=https://api.example.com
REACT_APP_ENV=development
```

## Build Configuration
### Webpack Configuration
Describe the configuration of Webpack for bundling:
- Entry Point: ./src/index.js
- Output Directory: ./dist
- Loaders: JavaScript, CSS, Images
- Plugins: HTMLWebpackPlugin, MiniCssExtractPlugin

Include a snippet or reference to your Webpack configuration file:
```JavaScript
module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      // Other loaders...
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
    // Other plugins...
  ],
};
```

### Babel Configuration
Describe Babel's configuration for transpiling JavaScript:
- Presets: @babel/preset-env, @babel/preset-react
- Plugins: Additional plugins like @babel/plugin-proposal-class-properties

Example .babelrc:
```json
{
  "presets": ["@babel/preset-env", "@babel/preset-react"],
  "plugins": ["@babel/plugin-proposal-class-properties"]
}
```
## Testing Configuration

### Unit Test
Configure testing libraries like Jest or Mocha:
- Framework: Jest
- Command: `npm test`
Example Jest configuration in package.json:
```json
"jest": {
  "setupFilesAfterEnv": ["<rootDir>/src/setupTests.js"],
  "testEnvironment": "jsdom"
}
```
### Integration Test
Integration testing involves testing the interactions between different components or modules of the application to ensure they work together as expected. Here’s a guide on how to conduct integration tests:

#### 1. Choose the Testing Framework
- Use a testing framework that supports integration tests. For JavaScript/React projects, you can use frameworks like Jest, Mocha, or Cypress.
#### 2. Identify Test Scenarios
- Identify key interactions between components or modules that need to be tested. For example, testing how the file upload component interacts with the transcription processing module.
#### 3. Set Up the Test Environment
- Ensure your testing environment is configured similarly to the production environment. This includes having access to the necessary APIs, databases, or services.
- Use test doubles (mocks, stubs, or spies) for any external services or APIs that your modules interact with.

#### 4. Write Integration Tests
- Write test cases that cover the interaction between modules. For example:
```JavaScript
test('File upload triggers transcription process', async () => {
  const file = new File(['audio content'], 'test-audio.mp3', { type: 'audio/mp3' });
  const uploadComponent = render(<UploadComponent />);
  
  await act(async () => {
    fireEvent.change(uploadComponent.getByTestId('file-upload'), { target: { files: [file] } });
    fireEvent.click(uploadComponent.getByText('Upload'));
  });
  
  expect(transcriptionProcess).toHaveBeenCalledWith(file);
});
```
- Test cases should cover all possible scenarios, including successful interactions and failure cases.

#### 5. Run the Tests
- Execute the integration tests using your testing framework’s command, e.g., `npm run test` for Jest.
- Review the test results and ensure that all tests pass.

#### 6. Continuous Integration
- Set up your CI/CD pipeline to run integration tests on every code push or pull request to ensure that new changes do not break existing integrations.


### Acceptance Test
Acceptance testing is performed to verify that the entire system meets the business requirements and works as expected. It’s usually the final testing phase before the product is released.
#### 1. Define Acceptance Criteria
- Clearly define the acceptance criteria for each feature based on user stories. This should be agreed upon by the stakeholders and the development team. 
#### 2. Prepare Test Cases
- Write test cases that cover the entire functionality of the feature, ensuring that all acceptance criteria are met.
- Test cases should be written in a way that mimics real user behavior, focusing on the end-to-end functionality.
- Example:
```gherkin
Feature: Transcribe Audio File
  Scenario: User uploads an audio file and receives a transcription
    Given the user has an audio file ready for transcription
    When the user uploads the audio file
    And selects the language as "English"
    Then the system should transcribe the file
    And the transcription should be sent to the user’s email
```
#### 3. Execute the Tests
- Manually execute the acceptance tests or use an automated tool like Cypress or Selenium if the tests are automated.
- Ensure all test cases pass and the system behaves as expected according to the acceptance criteria.
#### 4. Involve Stakeholders
- Involve stakeholders (e.g., product owners, end users, client) to review the test results.
- They should validate that the system meets the business requirements and is ready for release.

#### 5. Document the Results
- Document the results of the acceptance tests, including any issues encountered and how they were resolved.
- If all acceptance criteria are met, the feature is considered complete and ready for deployment.
#### 6. Sign-Off
- Obtain sign-off from stakeholders to confirm that the feature or product meets the required standards and is ready for production.

## Styling and Theming
### CSS Preprocessor
Describe the setup for a CSS preprocessor (e.g., SASS):
- Installation: `npm install sass --save-dev`
- Usage: Example of importing `.scss` files in React components.

### Theme Configuration
Outline the approach for theming (if applicable), e.g., using a theme provider or CSS variables.

## Version Control
### Branching Strategy
Describe the branching strategy (e.g., Git Flow, GitHub Flow):
- Main Branch: `main`
- Feature Branches: `feature/your-feature-name`
- Release Branches: `release/v1.0`
### Git Hooks
List any Git hooks in use, such as `pre-commit` hooks for linting.

## Deployment Configuration
### Hosting
Describe where the front-end will be deployed (e.g., AWS S3, Netlify):
- Build Command: `npm run build`
- Deployment Command: Commands or CI/CD pipeline steps for deployment.

### Continuous Integration
Include any CI/CD pipeline configurations (e.g., GitHub Actions, Travis CI).

## Best Practices
- **Code Formatting:** Use Prettier for consistent formatting.
- **Linting:** ESLint configuration for maintaining code quality.
- **Folder Structure:** Maintain a consistent folder structure for scalability.

## Troubleshooting
Common issues and their solutions:
- Issue: "Module not found"
    - Solution: Ensure that the dependency is installed and paths are correct.
- Issue: "EADDRINUSE: Address already in use"
    - Solution: Stop any process using the port or change the port in the configuration.
