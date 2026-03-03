package main

import (
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

const testInterval = 60 * time.Second

// Styles
var (
	titleStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color("#00FF00")).
			PaddingBottom(1)

	headerStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color("#FFFFFF"))

	labelStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#888888")).
			Width(20)

	valueStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#E0E0E0"))

	downloadStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#00FF00")).
			Bold(true)

	uploadStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FFFF00")).
			Bold(true)

	pingStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FF00FF"))

	statusStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#888888")).
			PaddingTop(1)

	historyHeaderStyle = lipgloss.NewStyle().
				Bold(true).
				Foreground(lipgloss.Color("#FFFFFF")).
				PaddingTop(1).
				PaddingBottom(0)

	errorStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FF0000"))

	borderStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#00FF00")).
			Padding(1, 2)
)

// Messages
type testResultMsg struct {
	entry *LogEntry
	err   error
}

type tickMsg time.Time

// Model
type model struct {
	latest    *LogEntry
	history   []LogEntry
	testing   bool
	countdown int
	err       error
	quitting  bool
}

func initialModel() model {
	return model{
		countdown: 0,
		testing:   true, // start with a test immediately
	}
}

func (m model) Init() tea.Cmd {
	return tea.Batch(runTest, tickEverySecond())
}

func runTest() tea.Msg {
	entry, err := RunSingleTest()
	return testResultMsg{entry: entry, err: err}
}

func tickEverySecond() tea.Cmd {
	return tea.Tick(time.Second, func(t time.Time) tea.Msg {
		return tickMsg(t)
	})
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			m.quitting = true
			return m, tea.Quit
		}

	case testResultMsg:
		m.testing = false
		m.countdown = int(testInterval.Seconds())
		if msg.err != nil {
			m.err = msg.err
		} else {
			m.err = nil
			m.latest = msg.entry
			m.history = append(m.history, *msg.entry)
			if len(m.history) > 5 {
				m.history = m.history[len(m.history)-5:]
			}
		}
		return m, tickEverySecond()

	case tickMsg:
		if m.testing {
			return m, tickEverySecond()
		}
		m.countdown--
		if m.countdown <= 0 {
			m.testing = true
			return m, tea.Batch(tea.Cmd(runTest), tickEverySecond())
		}
		return m, tickEverySecond()
	}

	return m, nil
}

func (m model) View() string {
	if m.quitting {
		return "Goodbye!\n"
	}

	var b strings.Builder

	// Title
	b.WriteString(titleStyle.Render("● Internet Speed Logger"))
	b.WriteString("\n")

	// Status
	if m.testing {
		b.WriteString(statusStyle.Render("Running speed test..."))
	} else {
		b.WriteString(statusStyle.Render(fmt.Sprintf("Next test in %ds", m.countdown)))
	}
	b.WriteString("\n\n")

	// Latest results
	if m.latest != nil {
		b.WriteString(headerStyle.Render("Latest Results"))
		b.WriteString("\n")
		b.WriteString(labelStyle.Render("Connection") + valueStyle.Render(m.latest.ConnType) + "\n")
		b.WriteString(labelStyle.Render("Network") + valueStyle.Render(m.latest.SSID) + "\n")
		b.WriteString(labelStyle.Render("Download") + downloadStyle.Render(fmt.Sprintf("↓ %.2f Mbps", m.latest.Download)) + "\n")
		b.WriteString(labelStyle.Render("Upload") + uploadStyle.Render(fmt.Sprintf("↑ %.2f Mbps", m.latest.Upload)) + "\n")
		b.WriteString(labelStyle.Render("Ping") + pingStyle.Render(fmt.Sprintf("%.2f ms", m.latest.Ping)) + "\n")
		b.WriteString(labelStyle.Render("Time") + valueStyle.Render(m.latest.Date+" "+m.latest.Time) + "\n")
	} else if m.err == nil {
		b.WriteString(valueStyle.Render("Waiting for first test result..."))
		b.WriteString("\n")
	}

	// Error
	if m.err != nil {
		b.WriteString("\n")
		b.WriteString(errorStyle.Render("Error: " + m.err.Error()))
		b.WriteString("\n")
	}

	// History
	if len(m.history) > 0 {
		b.WriteString(historyHeaderStyle.Render("Recent Tests"))
		b.WriteString("\n")
		for i := len(m.history) - 1; i >= 0; i-- {
			e := m.history[i]
			line := fmt.Sprintf("%s  ↓ %.1f  ↑ %.1f  %s",
				e.Time, e.Download, e.Upload, e.ConnType)
			b.WriteString(valueStyle.Render(line))
			b.WriteString("\n")
		}
	}

	b.WriteString("\n")
	b.WriteString(lipgloss.NewStyle().Foreground(lipgloss.Color("#555555")).Render("Press q to quit"))

	return borderStyle.Render(b.String())
}

func main() {
	// Set up logging
	logFile, err := os.OpenFile("wifi_speed_logger.log", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to open log file: %v\n", err)
		os.Exit(1)
	}
	defer logFile.Close()
	log.SetOutput(logFile)

	// Initialize CSV
	if err := InitializeCSV(); err != nil {
		fmt.Fprintf(os.Stderr, "Failed to initialize CSV: %v\n", err)
		os.Exit(1)
	}

	// Run TUI
	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error running program: %v\n", err)
		os.Exit(1)
	}
}
