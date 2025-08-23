import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Card,
  CardContent,
  Stack,
  Snackbar,
  Alert,
} from "@mui/material";
import axios from "axios";
import TestRunner from "./TestReport";

export default function CalculatorForm() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [calledCount, setCalledCount] = useState(0);
  const [error, setError] = useState("");
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [testResults, setTestResults] = useState([]);
  const [testSummary, setTestSummary] = useState(null);
  const [resetTrigger, setResetTrigger] = useState(0);
const handleResetAll = () => {
    setTestResults([]);
    setTestSummary(null);
    setResetTrigger((t) => t + 1);
};
const handleCalculate = async () => {
  try {
    // Replace literal "\n" with actual newline character
    const formattedInput = input.replace(/\\n/g, "\n");

    const { data } = await axios.post("/api/add", { input: formattedInput });

    if (data.ok) {
      setResult(data.result);
      setCalledCount(data.calledCount);
      setError("");
    } else {
      setError(data.error);
    }
  } catch (e) {
    setError(e.response?.data?.error || e.message);
  }
};


  const handleReset = async () => {
    try {
      const { data } = await axios.post("/api/reset");
      if (data.ok) {
        setInput("");
        setResult(null);
        setError("");
        setCalledCount(data.calledCount);
        setSnackbarOpen(true);
        handleResetAll();  
      }
    } catch (e) {
      console.error("Reset failed", e);
    }
  };

  return (
    <Card sx={{ p: 3, borderRadius: 3, boxShadow: 3, minWidth: 320 }}>
      <CardContent>
        <Stack spacing={2}>
          <TextField
            label="Numbers Input"
            variant="outlined"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            fullWidth
          />
          <Stack direction="row" spacing={2}>
            <Button variant="contained" onClick={handleCalculate}>
            Calculate Sum
            </Button>
            <Button variant="outlined" color="secondary" onClick={handleReset}>
              Reset
            </Button>
          </Stack>

          {result !== null && (
            <Typography variant="body1" color="primary">
              Result: {result}
            </Typography>
          )}
          {error && (
            <Typography variant="body2" color="error">
              {error}
            </Typography>
          )}

          <Typography
            variant="caption"
            sx={{
              mt: 1,
              display: "inline-block",
              px: 1.5,
              py: 0.5,
              borderRadius: 10,
              bgcolor: "grey.100",
            }}
          >
            Add called: <strong>{calledCount} times</strong>
          </Typography>
        </Stack>
        <TestRunner
            results={testResults}
            setResults={setTestResults}
            summary={testSummary}
            setSummary={setTestSummary}
            resetTrigger={resetTrigger}
          />
      </CardContent>

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert severity="success" onClose={() => setSnackbarOpen(false)}>
          Calculator & Tests reset successfully
        </Alert>
      </Snackbar>
    </Card>
  );
}
