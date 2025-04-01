import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import About from "./about";

describe("About Component", () => {
    test("renders the navigation bar correctly", () => {
        render(
            <MemoryRouter>
                <About />
            </MemoryRouter>
        );

        // Check if the logo is rendered
        expect(screen.getByAltText("logo")).toBeInTheDocument();

        // Check if the navigation links are present
        expect(screen.getByRole("link", { name: /About/i })).toBeInTheDocument();
        expect(screen.getByRole("link", { name: /Transcription/i })).toBeInTheDocument();
        expect(screen.getByRole("link", { name: /History/i })).toBeInTheDocument();
    });

    test("renders the hero section with title and description", () => {
        render(
            <MemoryRouter>
                <About />
            </MemoryRouter>
        );

        // Fixing the title check by correcting the spelling error
        expect(
            screen.getByText((content, element) =>
                content.startsWith("Transcription Aide Platform")
            )
        ).toBeInTheDocument();

        // Fixing the description check by matching a partial text
        expect(
            screen.getByText((content) =>
                content.includes("Everything you need to transcribe audio files")
            )
        ).toBeInTheDocument();
    });

    test("renders the tools section with all required cards", () => {
        render(
            <MemoryRouter>
                <About />
            </MemoryRouter>
        );

        // Check section title
        expect(
            screen.getByText(/All the tools you need for transcription in one place/i)
        ).toBeInTheDocument();

        // Check each tool card's title using precise matching
        expect(screen.getAllByText(/Upload your files/i)[0]).toBeInTheDocument();
        expect(screen.getAllByText(/Transcribe/i)[0]).toBeInTheDocument();
        expect(screen.getAllByText(/Get Results/i)[0]).toBeInTheDocument();
    });

    test("renders all navigation links inside tool cards", () => {
        render(
            <MemoryRouter>
                <About />
            </MemoryRouter>
        );

        // Improved way to check links using `getAllByRole` due to multiple matches
        const uploadLinks = screen.getAllByRole("link", { name: /Upload your files/i });
        expect(uploadLinks[0]).toHaveAttribute("href", "/Transcription");

        const transcribeLinks = screen.getAllByRole("link", { name: /Transcribe/i });
        expect(transcribeLinks[0]).toHaveAttribute("href", "/Transcription");

        const resultsLinks = screen.getAllByRole("link", { name: /Get Results/i });
        expect(resultsLinks[0]).toHaveAttribute("href", "/historylogin");
    });

    test("renders tool section images correctly", () => {
        render(
            <MemoryRouter>
                <About />
            </MemoryRouter>
        );

        // Check if all tool images exist
        expect(screen.getByAltText("file_upload_icon")).toBeInTheDocument();
        expect(screen.getByAltText("transcribe_icon")).toBeInTheDocument();
        expect(screen.getByAltText("result_icon")).toBeInTheDocument();
        expect(screen.getAllByAltText("arrow")).toHaveLength(2); // Two arrow images
    });

    test("renders the footer correctly", () => {
        render(
            <MemoryRouter>
                <About />
            </MemoryRouter>
        );

        // Check if footer text is present
        expect(
            screen.getByText(/2023 TAP. All Rights Reserved./i)
        ).toBeInTheDocument();
    });

    test("handles location state correctly", () => {
        const demoData = { sample: "test data" };
        const consoleSpy = jest.spyOn(console, "log"); // Mock console.log

        render(
            <MemoryRouter initialEntries={[{ pathname: "/about", state: { demoData } }]}>
                <About />
            </MemoryRouter>
        );

        // Check if console logs the state
        expect(consoleSpy).toHaveBeenCalledWith(demoData);
        consoleSpy.mockRestore(); // Restore console log
    });
});
