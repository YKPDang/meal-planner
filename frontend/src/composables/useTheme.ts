import { useTheme as useVuetifyTheme } from "vuetify";
import { computed } from "vue";

export function useTheme() {
  const { global } = useVuetifyTheme();

  const isDark = computed({
    get: () => global.name.value === "dark",
    set: (value: boolean) => {
      global.name.value = value ? "dark" : "light";
    }
  });

  const toggle = () => {
    isDark.value = !isDark.value;
  };

  return {
    isDark,
    toggle
  };
}
