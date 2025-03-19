import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import Process from './process';

// Mocking useNavigate from react-router-dom
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: jest.fn(),
}));

describe('Process Component', () => {
    let mockNavigate;

    beforeEach(() => {
        mockNavigate = jest.fn();
        useNavigate.mockReturnValue(mockNavigate);
    });

    test('renders process component with status section', () => {
        render(
            <MemoryRouter>
                <Process />
            </MemoryRouter>
        );

        // Check if the "Status" section is rendered correctly
        expect(screen.getByText(/Status.../i)).toBeInTheDocument();
        expect(screen.getByText(/Your place in the queue is:/i)).toBeInTheDocument();
        expect(screen.getByText(/Estimate time:/i)).toBeInTheDocument();
    });

    test('renders file processing message', () => {
        render(
            <MemoryRouter>
                <Process />
            </MemoryRouter>
        );

        // Check if the file processing message is displayed
        expect(screen.getByText(/The file\(s\) is currently being processed/i)).toBeInTheDocument();
    });

    test('renders navigation links', () => {
        render(
            <MemoryRouter>
                <Process />
            </MemoryRouter>
        );

        // Check if navigation links exist
        expect(screen.getByRole('link', { name: /About/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /Transcription/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /History/i })).toBeInTheDocument();
    });

    test('calls navigate when clicking "Transcribe a New Task" button', () => {
        render(
            <MemoryRouter>
                <Process />
            </MemoryRouter>
        );

        const transcribeButton = screen.getByRole('button', { name: /Transcribe a New Task/i });
        fireEvent.click(transcribeButton);

        // Check if navigate function was called with correct argument
        expect(mockNavigate).toHaveBeenCalledWith('/transcription');
    });
});
