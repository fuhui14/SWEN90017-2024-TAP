# Git Commit Standards

## 1. Branch Naming Conventions

### 1.1 Main Branch
- `main`: The primary production branch, always in a stable and deployable state, used for release and deployment.

### 1.2 Development Branches
- `dev-backend`: Main development branch for backend. All backend feature branches should be branched off from here and merged back after completion.
- `dev-frontend`: Main development branch for frontend. All frontend feature branches should be 
  branched off from here and merged back after completion.

### 1.3 Feature Branches
- `feature/frontend/<short-description>`: Used for developing new frontend features. Example: 
  `feature/frontend/upload-flie`
- `feature/backend/<short-description>`: Used for developing new backend features. The short 
  description must align with the frontend. Example: 
  `feature/backend/upload-file`

### 1.4 Release Branches (optional)
- `release/<version-number>`: Used for preparing a new release. Example: `release/sprint 1`

## 2. Commit Message Standards

### 2.1 Commit Message Format
- Each commit should have a clear and concise message, including the following parts:  
  `short description`  
  `(optional) detailed description`

### 2.2 Examples
- `add file upload functionality`  
  `(optional) Implemented basic file upload functionality.`

## 3. Code Review Process
All code changes need to undergo a code review to ensure code quality and consistency.

### 3.1 Pull Request
- Create a pull request from the feature branch to the `dev-backend` or `dev-frontend` branch.
- Clearly describe the changes and purpose in the pull request description.

### 3.2 Code Review
- At least one other developer should review the code.
- Reviewers should check the correctness and style consistency.

### 3.3 Feedback and Modification
- Address the reviewers' feedback and respond within the pull request.
- Reviewers will re-review the changes until they are approved.

### 3.4 Merge
- The pull request can be merged only after approval.
- After merging, the corresponding feature branch should be deleted to keep the branch management clean.

## 4 Additional Guidelines

### Branch Protection
- Protect the `main`, `dev-backend`, and `dev-frontend` branches.
- Direct pushes are prohibited. All changes must go through a pull request.
