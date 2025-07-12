import { useMemo } from 'react';
import { ThemeProvider as MuiThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#3e7349' },
    secondary: { main: '#4e5aaa' },
    error: { main: '#b00020' },
    background: {
      paper: '#f8f9fa',
      default: '#deeae3',
      contrast: '#9ed9b7',
    },
    text: {
      primary: '#212121',
      secondary: '#616161',
    },
    custom: {
      accent: '#f6e3d1',
      border: '#394a3c',
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
      '--color-background-contrast': palette.background.contrast,
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
