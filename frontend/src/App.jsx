import React, { useState } from "react";
import { Container, Grid } from "@mui/material";
import CalculatorForm from "./components/CalculatorForm";
import TestRunner from "./components/TestReport";
import Features from "./components/Features";

export default function App() {
// Reset everything (calculator + tests)

  return (
    <Container maxWidth="lg" minHeight="lg" sx={{ py: 5 }}>
      <Grid container spacing={3}>
        <Grid item xs={0} md={2}></Grid>
        <Grid item xs={12} md={8}>
          <CalculatorForm />
        </Grid>
        <Grid item xs={12}>
          <Features />
        </Grid>
      </Grid>
    </Container>
  );
}
