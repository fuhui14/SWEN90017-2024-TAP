# Unit Test: App Component


## 1. App.test.js

### **Test Case 1: Renders Transpage component on default route (`/`)**
- **Description**: Ensures that when navigating to the root (`/`), the `Transpage` component is rendered correctly.
- **Expected Behavior**: The page should display the text `Select transcription language`.
- **Test Code**:
  ```javascript
  test('renders Transpage component on default route ("/")', () => {
      render(
          <MemoryRouter initialEntries={['/']}>
              <App />
          </MemoryRouter>
      );
      expect(screen.getByText(/Select transcription language/i)).toBeInTheDocument();
  });
  ```

### **Test Case 2: Renders Transpage component on `/transcription` route**
- **Description**: Ensures that navigating to `/transcription` renders `Transpage`.
- **Expected Behavior**: The page should display the text `Select transcription language`.
- **Test Code**:
  ```javascript
  test('renders Transpage component on "/transcription" route', () => {
      render(
          <MemoryRouter initialEntries={['/transcription']}>
              <App />
          </MemoryRouter>
      );
      expect(screen.getByText(/Select transcription language/i)).toBeInTheDocument();
  });
  ```

### **Test Case 3: Renders Process component on `/process` route**
- **Description**: Ensures that navigating to `/process` correctly renders the `Process` component.
- **Expected Behavior**: The page should display the text `status` and `your place in the queue`.
- **Test Code**:
  ```javascript
  test('renders Process component on "/process" route', () => {
      render(
          <MemoryRouter initialEntries={['/process']}>
              <App />
          </MemoryRouter>
      );
      expect(screen.getByText(/status/i)).toBeInTheDocument();
      expect(screen.getByText(/your place in the queue/i)).toBeInTheDocument();
  });
  ```

### **Test Case 4: Renders navigation link for transcription**
- **Description**: Ensures the transcription navigation link is displayed correctly.
- **Expected Behavior**: The page should contain a link labeled `Transcription`.
- **Test Code**:
  ```javascript
  test('renders navigation link for transcription', () => {
      render(
          <MemoryRouter>
              <App />
          </MemoryRouter>
      );
      expect(screen.getByRole('link', { name: /Transcription/i })).toBeInTheDocument();
  });
  ```
### Test Result
All **4 test cases** for the `App` component have passed successfully, as shown in the test result screenshot below. These tests cover the application's routing behavior and the visibility of core UI elements like links and labels on different routes (`/`, `/transcription`, `/process`).

On the right side of the report, the code coverage metrics indicate:

- ✅ **100% statement, branch, function, and line coverage** for `App.js`, meaning all executable paths in this file are tested.
- ⚠️ **Partial or missing coverage in `index.js`**, with uncovered lines between lines 8 and 20. This is expected, as `index.js` often contains boilerplate code like React root rendering, which typically requires integration testing rather than unit testing.

Overall, this confirms that the routing logic and rendering of components within `App.js` are **robust and well-tested**.

![image](https://github.com/user-attachments/assets/acbd2cd7-d3c7-419e-8834-2c913ae91f9b)

---

## 2. transpage.test.js

### **Test Case 1: Renders email input and validates correct email format**
- **Description**: Ensures the email input field is rendered and validates input correctly.
- **Expected Behavior**: A valid email should display a checkmark icon.
- **Test Code**:
  ```javascript
  test('renders email input and validates correct email format', () => {
      render(
          <MemoryRouter>
              <Transpage />
          </MemoryRouter>
      );
      const emailInput = screen.getByPlaceholderText(/Enter your email/i);
      expect(screen.queryByAltText(/Valid email/i)).not.toBeInTheDocument();
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      expect(screen.getByAltText(/Valid email/i)).toBeInTheDocument();
  });
  ```

### **Test Case 2: Renders file input and allows file upload**
- **Description**: Ensures that files can be uploaded successfully.
- **Expected Behavior**: The uploaded file should appear in the file list.
- **Test Code**:
  ```javascript
  test('renders file input and allows file upload', () => {
      render(
          <MemoryRouter>
              <Transpage />
          </MemoryRouter>
      );
      const fileInput = screen.getByLabelText(/Drag a file\(s\) here or choose a file to upload/i);
      const testFile = new File(['dummy content'], 'test.mp3', { type: 'audio/mpeg' });
      fireEvent.change(fileInput, { target: { files: [testFile] } });
      expect(screen.getByText(/test.mp3/i)).toBeInTheDocument();
  });
  ```

### **Test Case 3: Allows user to delete an uploaded file**
- **Description**: Ensures that users can remove files from the uploaded list.
- **Expected Behavior**: After clicking the delete button, the file should be removed.
- **Test Code**:
  ```javascript
  test('allows user to delete an uploaded file', async () => {
      render(
          <MemoryRouter>
              <Transpage />
          </MemoryRouter>
      );
      const fileInput = screen.getByLabelText(/Drag a file\(s\) here or choose a file to upload/i);
      const testFile = new File(['dummy content'], 'test.mp3', { type: 'audio/mpeg' });
      fireEvent.change(fileInput, { target: { files: [testFile] } });
      expect(screen.getByText(/test.mp3/i)).toBeInTheDocument();
      const deleteButton = screen.getByRole('button', { name: /×/i });
      fireEvent.click(deleteButton);
      await waitFor(() => expect(screen.queryByText(/test.mp3/i)).not.toBeInTheDocument());
  });
  ```

### **Test Case 4: Displays an alert if required fields are missing on confirm**
- **Description**: Ensures that clicking confirm without entering required data triggers an alert.
- **Expected Behavior**: The alert message should appear.
- **Test Code**:
  ```javascript
  test('displays an alert if required fields are missing on confirm', () => {
      window.alert = jest.fn();
      render(
          <MemoryRouter>
              <Transpage />
          </MemoryRouter>
      );
      fireEvent.click(screen.getByRole('button', { name: /Confirm/i }));
      expect(window.alert).toHaveBeenCalledWith('Please fill out all required fields.');
  });
  ```

### **Test Case 5: Navigates to transcription result page after successful confirmation**
- **Description**: Ensures that a successful form submission redirects the user.
- **Expected Behavior**: The `useNavigate` function should be called with `/transcription/transcriptionresult`.
- **Test Code**:
  ```javascript
  test('navigates to transcription result page after successful confirmation', async () => {
      render(
          <MemoryRouter>
              <Transpage />
          </MemoryRouter>
      );
      const emailInput = screen.getByPlaceholderText(/Enter your email/i);
      const fileInput = screen.getByLabelText(/Drag a file\(s\) here or choose a file to upload/i);
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.change(fileInput, { target: { files: [new File(['dummy'], 'test.mp3', { type: 'audio/mpeg' })] } });
      fireEvent.click(screen.getByRole('button', { name: /Confirm/i }));
      await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/transcription/transcriptionresult', expect.any(Object)));
  });
  ```
### Test Result
All **5 test cases** for the `Transpage` component passed successfully. These cases thoroughly cover essential user interactions such as email input validation, file upload handling, file removal, error alerts, and navigation on successful submission.

On the right side of the test coverage report, we see that:

- `transpage.js` achieves **71.29% statement coverage**, **53.57% branch coverage**, and **71.84% line coverage**.

This reflects that while the major functional paths are covered, there are still areas—especially conditional branches and deeper UI states—that require more specific test cases (e.g., error responses from fetch, multiple file uploads, or invalid file types).

Despite the uncovered lines, the current tests give us **high confidence** in the component's core logic and user experience under standard usage conditions.
![image](https://github.com/user-attachments/assets/80c7864f-d508-49c0-ac4b-408f6f9a9f7a)

