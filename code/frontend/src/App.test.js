import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

describe('App Component', () => {
    test('renders Transpage component on default route ("/")', () => {
        render(
            <MemoryRouter initialEntries={['/']}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Select transcription language/i)).toBeInTheDocument();
    });

    test('renders Transpage component on "/transcription" route', () => {
        render(
            <MemoryRouter initialEntries={['/transcription']}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/Select transcription language/i)).toBeInTheDocument();
    });

    test('renders Process component on "/process" route', () => {
        render(
            <MemoryRouter initialEntries={['/process']}>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByText(/status/i)).toBeInTheDocument();
        expect(screen.getByText(/your place in the queue/i)).toBeInTheDocument();
    });

    // test('renders TranscriptionResult component on "/transcription/transcriptionresult" route', () => {
    //     render(
    //         <MemoryRouter initialEntries={['/transcription/transcriptionresult']}>
    //             <App />
    //         </MemoryRouter>
    //     );
    //
    //     expect(screen.getByText(/Transcription results/i)).toBeInTheDocument();
    // });

    test('renders navigation link for transcription', () => {
        render(
            <MemoryRouter>
                <App />
            </MemoryRouter>
        );

        expect(screen.getByRole('link', { name: /Transcription/i })).toBeInTheDocument();
    });
});
