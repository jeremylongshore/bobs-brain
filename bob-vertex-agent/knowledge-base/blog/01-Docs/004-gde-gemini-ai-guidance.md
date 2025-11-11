# GEMINI.md: Jeremy Longshore's Portfolio & Blog

## Project Overview

This directory contains the source code for Jeremy Longshore's personal portfolio and blog, located at [jeremylongshore.com](https://jeremylongshore.com).

It is a static website built with the [Hugo](https://gohugo.io/) static site generator. The content is written in Markdown and the site is deployed via Netlify. The `hugo.toml` file indicates the use of the `hermit-v2` theme.

The site serves as a professional portfolio showcasing projects, work experience, and technical blog posts related to AI development and DevOps.

## Building and Running

The project's `README.md` provides clear instructions for local development.

### Running the Development Server

To run a local server with live reloading and see draft posts, use the following command:

```bash
hugo server -D
```

### Building for Production

To generate the static site into the `public/` directory, run:

```bash
hugo
```
This is the command Netlify uses to build the site before deployment.

## Development Conventions

### Creating New Content

New blog posts can be created using the `hugo new` command. Based on the project structure, new posts should be created in the `content/en/blogs/` directory.

```bash
hugo new content/en/blogs/your-new-post-title.md
```

### Project Structure

The project follows a standard Hugo layout:

*   `content/`: Contains all Markdown content for the site, including pages and blog posts.
*   `themes/`: Contains the Hugo theme used for styling and layout (`hermit-v2`).
*   `static/`: Holds static assets like images and CSS.
*   `public/`: The output directory where the generated static site is placed (this directory is not tracked by Git).
*   `hugo.toml`: The main configuration file for the Hugo site.
*   `netlify.toml`: Configuration file for deploying the site on Netlify.
