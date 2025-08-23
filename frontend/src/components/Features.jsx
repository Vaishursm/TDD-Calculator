import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";

const features = [
  {
    title: "Basic Requirements",
    color: "success.main",
    items: [
      "Handle 0, 1, or 2 numbers",
      "Return sum (empty string = 0)",
      "Handle unknown amount of numbers",
      "Support newlines between numbers",
    ],
  },
  {
    title: "Advanced Features",
    color: "warning.main",
    items: [
      "Custom delimiters: //[delimiter]\\n",
      "Negative number exceptions",
      "Multiple negatives in error",
      "GetCalledCount() method",
      "Decimal numbers not allowed",
    ],
  },
  {
    title: "Extended Features",
    color: "info.main",
    items: [
      "Ignore numbers > 1000",
      "Multi-character delimiters",
      "Multiple delimiters",
      "Complex delimiter combinations",
    ],
  },
];

export default function Features() {
  return (
    <Grid container spacing={3} sx={{ mt: 2 }}>
      {features.map((f, idx) => (
        <Grid item xs={12} md={4} key={idx}>
          <Card
            sx={{
              borderRadius: 3,
              boxShadow: 2,
              height: "100%",                // ✅ ensure equal height
              display: "flex",
              flexDirection: "column",
            }}
          >
            <CardContent sx={{ flexGrow: 1 }}>
              <Typography
                variant="h6"
                gutterBottom
                sx={{ color: f.color, fontWeight: "bold" }}
              >
                {f.title}
              </Typography>
              <List dense>
                {f.items.map((item, i) => (
                  <ListItem key={i}>
                    <ListItemText primary={item} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}
