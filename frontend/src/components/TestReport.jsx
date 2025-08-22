import React, { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import axios from "axios";

export default function TestRunner(...props) {
  const resetTrigger = props[0]["resetTrigger"];
  const [results, setResults] = useState([]);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    if (resetTrigger) {
        console.log("TestRunner reset triggered");
      setResults([]);
      setSummary(null);
    }
  }, [resetTrigger]);

  const handleRunTests = async () => {
    try {
      const { data } = await axios.post("/api/run-tests", {});
      setResults(data.results);
      setSummary(data.summary);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <Card
      sx={{
        p: 2,
        borderRadius: 3,
        boxShadow: 3,
        minWidth: 320,
        background: "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)",
        color: "white",
      }}
    >
      <CardContent>
        <Button
          variant="contained"
          sx={{ bgcolor: "rgba(255,255,255,0.2)", mb: 2 }}
          onClick={handleRunTests}
        >
          Run All Tests
        </Button>

        {summary ? (
          <>
            <Typography variant="body2">
              Total: {summary.total} | Passed: {summary.passed} | Failures:{" "}
              {summary.failures}
            </Typography>
            <List dense>
              {results.map((r, idx) => (
                <ListItem key={idx} sx={{ color: "white" }}>
                  <ListItemText
                    primary={`${r.name} — ${r.status.toUpperCase()}`}
                    secondary={r.message || ""}
                  />
                </ListItem>
              ))}
            </List>
          </>
        ) : (
          <Typography variant="caption">
            <br></br>Click "Run All Tests" to see results
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}
