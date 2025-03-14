# Frontend Test Specification

## 1. Testing Tools and Dependencies

### Jest
Jest is a JavaScript testing framework used for running test cases and generating reports. It comes pre-configured with Create React App, but for manual setup, install it using:

```sh
npm install --save-dev jest
```

Jest supports custom configurations through a `jest.config.js` file if needed. However, in most cases, the default settings are sufficient.

### React Testing Library (RTL)
React Testing Library is used to test React components by rendering them and simulating user interactions. Install it with:

```sh
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

`@testing-library/jest-dom` provides additional DOM assertions like `.toBeInTheDocument()`. If using Create React App, ensure `@testing-library/jest-dom` is imported in `setupTests.js`.

## 2. Running Unit Tests

### Running All Tests
To run all test cases, use:

```sh
npm test
```


This starts Jest in watch mode, allowing you to rerun tests upon changes. Use `a` to run all tests or `q` to quit.

### Running a Specific Test File
To run a specific test file, use:

```sh
npm test <test-file-name>
```




### Viewing Test Coverage
Generate a coverage report with:

```sh
npm test -- --coverage
```

This produces a summary in the terminal and an HTML report in the `coverage` folder, accessible via `coverage/lcov-report/index.html`.

## 3. Unit Testing Goals

- **Ensure Component Functionality**: Verify components behave as expected under various inputs and states.
- **Validate User Interactions**: Simulate user actions (clicks, inputs, selections) and check corresponding responses.
- **Confirm API Calls**: Ensure API requests have correct parameters and responses are handled properly.
- **Prevent Regressions**: Catch unintended changes due to new code modifications.

