import { ThemeDefinition } from "vuetify";

export const dark: ThemeDefinition = {
  dark: true,
  colors: {
    background: "#121212",
    surface: "#1E1E1E",
    "surface-bright": "#2C2C2C",
    "surface-variant": "#252525",
    primary: "#7C8FFF",
    "primary-darken-1": "#6A7DD8",
    secondary: "#FFB74D",
    accent: "#FF8A65",
    "on-background": "#E0E0E0",
    error: "#CF6679",
    info: "#64B5F6",
    success: "#81C784",
    warning: "#FFB74D"
  }
};

export const light: ThemeDefinition = {
  dark: false,
  colors: {
    background: "#FAFAFA",
    surface: "#FFFFFF",
    "surface-bright": "#F5F5F5",
    "surface-variant": "#EEEEEE",
    primary: "#3F51B5",
    "primary-darken-1": "#334296",
    secondary: "#F4B400",
    accent: "#FF7043",
    "on-background": "#212121",
    error: "#d32f2f",
    info: "#1976d2",
    success: "#2e7d32",
    warning: "#ed6c02"
  }
};
