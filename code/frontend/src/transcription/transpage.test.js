import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Transpage from './transpage';

// Mock `useNavigate` from react-router-dom
import { useNavigate } from 'react-router-dom';
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: jest.fn(),
}));

describe('Transpage Component', () => {
    let mockNavigate;

    beforeEach(() => {
        mockNavigate = jest.fn();
        useNavigate.mockReturnValue(mockNavigate);
    });

    test('renders email input and validates correct email format', () => {
        render(
            <MemoryRouter>
                <Transpage />
            </MemoryRouter>
        );

        // Get the email input field
        const emailInput = screen.getByPlaceholderText(/Enter your email/i);

        // Initially, there should be no valid email indicator
        expect(screen.queryByAltText(/Valid email/i)).not.toBeInTheDocument();

        // Enter a valid email
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });

        // Check if the valid email indicator appears
        expect(screen.getByAltText(/Valid email/i)).toBeInTheDocument();
    });

    test('renders file input and allows file upload', () => {
        render(
            <MemoryRouter>
                <Transpage />
            </MemoryRouter>
        );

        const fileInput = screen.getByLabelText(/Drag a file\(s\) here or choose a file to upload/i);
        const testFile = new File(['dummy content'], 'test.mp3', { type: 'audio/mpeg' });

        // Upload file
        fireEvent.change(fileInput, { target: { files: [testFile] } });

        // Check if the uploaded file appears in the file list
        expect(screen.getByText(/test.mp3/i)).toBeInTheDocument();
    });

    test('allows user to delete an uploaded file', async () => {
        render(
            <MemoryRouter>
                <Transpage />
            </MemoryRouter>
        );

        const fileInput = screen.getByLabelText(/Drag a file\(s\) here or choose a file to upload/i);
        const testFile = new File(['dummy content'], 'test.mp3', { type: 'audio/mpeg' });

        // Upload file
        fireEvent.change(fileInput, { target: { files: [testFile] } });

        // Ensure file appears
        expect(screen.getByText(/test.mp3/i)).toBeInTheDocument();

        // Click delete button
        const deleteButton = screen.getByRole('button', { name: /×/i });
        fireEvent.click(deleteButton);

        // Ensure file is removed
        await waitFor(() => expect(screen.queryByText(/test.mp3/i)).not.toBeInTheDocument());
    });

    test('displays an alert if required fields are missing on confirm', () => {
        window.alert = jest.fn(); // Mock alert

        render(
            <MemoryRouter>
                <Transpage />
            </MemoryRouter>
        );

        // Click the confirm button without entering email or uploading files
        const confirmButton = screen.getByRole('button', { name: /Confirm/i });
        fireEvent.click(confirmButton);

        // Ensure alert is triggered
        expect(window.alert).toHaveBeenCalledWith('Please fill out all required fields.');
    });

    test('navigates to transcription result page after successful confirmation', async () => {
        render(
            <MemoryRouter>
                <Transpage />
            </MemoryRouter>
        );

        const emailInput = screen.getByPlaceholderText(/Enter your email/i);
        const fileInput = screen.getByLabelText(/Drag a file\(s\) here or choose a file to upload/i);
        const confirmButton = screen.getByRole('button', { name: /Confirm/i });

        const testFile = new File(['dummy content'], 'test.mp3', { type: 'audio/mpeg' });

        // Enter valid email
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });

        // Upload a file
        fireEvent.change(fileInput, { target: { files: [testFile] } });

        // Mock successful API response
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ transcription: [{ speaker: 1, text: 'Hello world' }] }),
            })
        );

        // Click confirm
        fireEvent.click(confirmButton);

        // Wait for navigation to be called
        await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/transcription/transcriptionresult', expect.any(Object)));
    });
});
