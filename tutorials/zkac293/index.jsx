import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { ThemeProvider } from "@chakra-ui/core";

ReactDOM.render(
  <ThemeProvider>
    <App />
  </ThemeProvider>,
  document.getElementById("root")
);