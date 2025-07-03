use dotenvy::dotenv;
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::env;
use std::io::{self, Write};

#[derive(Serialize, Deserialize)]            
struct ContentPart {
    text: String,
}

#[derive(Serialize)]
struct ContentRequest {
    contents: Vec<Content>,
}

#[derive(Serialize)]
struct Content {
    parts: Vec<ContentPart>,
    role: String,
}

#[derive(Deserialize)]
struct GeminiResponse {
    candidates: Vec<GeminiCandidate>,
}

#[derive(Deserialize)]
struct GeminiCandidate {
    content: ContentResponse,
}

#[derive(Deserialize)]
struct ContentResponse {
    parts: Vec<ContentPart>,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok();

    let api_key = env::var("GEMINI_API_KEY")
        .expect("GEMINI_API_KEY not set in .env");

    // ── Read multiline user input ──
    let mut user_input = String::new();
    println!("Enter text to paraphrase. Once you enter your text, hit enter again:");
    loop {
        print!("> ");
        io::stdout().flush()?;
        let mut line = String::new();
        io::stdin().read_line(&mut line)?;
        if line.trim().is_empty() {
            break;
        }
        user_input.push_str(&line);
    }

    if user_input.trim().is_empty() {
        println!("No input provided. Exiting.");
        return Ok(());
    }

    // ─── Build Gemini prompt ────
    let prompt = format!(
        "Paraphrase and improve the following text. Keep the meaning but enhance clarity and grammar:\n\n{}",
        user_input.trim()
    );

    let request_body = ContentRequest {
        contents: vec![Content {
            role: "user".to_string(),
            parts: vec![ContentPart { text: prompt }],
        }],
    };

    // ─── Send request ────
    let client = Client::new();
    let url = format!(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={}",
        api_key
    );

    println!("\nSending request to Gemini...");

    let response = client.post(&url).json(&request_body).send().await?;

    if !response.status().is_success() {
        eprintln!("Request failed: {}", response.status());
        let body = response.text().await?;
        eprintln!("Response body: {}", body);
        return Ok(());
    }

    // ─── Parse response ───
    let json: GeminiResponse = response.json().await?;

    if let Some(first) = json.candidates.first() {
        let paraphrased = first
            .content
            .parts
            .iter()
            .map(|p| p.text.as_str())
            .collect::<Vec<&str>>()
            .join("\n");

        println!("\n=== Paraphrased Text ===\n{}", paraphrased);
    } else {
        println!("No response candidates returned.");
    }

    Ok(())
}
