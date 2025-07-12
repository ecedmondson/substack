import { useMemo } from 'react';
import { ThemeProvider as MuiThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#6200ea' },
    secondary: { main: '#03dac6' },
    error: { main: '#b00020' },
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
    text: {
      primary: '#212121',
      secondary: '#616161',
    },
    custom: {
      accent: '#ffcc00',
      border: '#e0e0e0',
    },
  },
});

const ThemeProvider = ({ children }) => {
  const cssVars = useMemo(() => {
    const palette = theme.palette;
    return {
      '--color-primary': palette.primary.main,
      '--color-secondary': palette.secondary.main,
      '--color-error': palette.error.main,
      '--color-background': palette.background.default,
      '--color-surface': palette.background.paper,
      '--color-text-primary': palette.text.primary,
      '--color-text-secondary': palette.text.secondary,
      '--color-border': palette.custom?.border || '#e0e0e0',
      '--color-accent': palette.custom?.accent || '#ffcc00',
    };
  }, []);

  return (
    <MuiThemeProvider theme={theme}>
      <CssBaseline />
      <div id="theme-root" style={cssVars}>
        {children}
      </div>
    </MuiThemeProvider>
  );
};


export default ThemeProvider;
