Jurassic PERTS
==========

Jurassic PERTS is a tool for generating PDF files from HTML using standard
styling used by the PERTS organization.

## About Styling

DocRaptor provides an API to render PDF document from HTML using Prince XML
software.

### DocRaptor

To get better acquianted with DocRaptor and their API you can take a look at
[their documentation](http://docraptor.com/).

### Prince XML

Prince XML is a powerful library for creating PDF documents. They provide a
wide variety of incredibly useful styles such as column formatting and
footnotes. Learn more about Prince in their [guide](https://www.princexml.com/doc/)

## Components

A variety of basic styles are covered by the CSS rules in 
`/templates/reports/_styles.html`. These are injected in any file by default
but can be turned off if you'd like to use your own.

### Cover page

```
<div id="cover_page">
  <img src="https://s3.amazonaws.com/PERTS/images/perts-logo.png" />
  <h1 class="title">
    Example Document
  </h1>
  <h3>
    {{ monthyear }}
  </h3>
</div>
```

### Table of Contents

The Table of Contents will automatically generate page numbers and 

### Figures

Figures can be inserted anywhere in the document using a `figure` element.

Example:
```
<figure>
  <img src="https://acceptance-dot-yellowstoneplatform.appspot.com/static/images/home/success_rate_7_semesters_gms.png" />
  <figcaption>Something about this.</figcaption>
</figure>
```

Since drawing figures in html can be tricky, the easiest way to add figures is
through `img` elements. Be sure that the image source is available at a public
url (should begin with 'http').

Please note that the standard figure will span 75% of the page width. There are
additional classes `class="half-width"` and `class="full-width"` that can be
added to the `figure` element to adjust this setting.

Figure captions should be placed after the `img` element inside of the `figure`
using the following format: `<figcaption>Caption text</figcaption>`

### Tables



Be sure to use `th` elements instead of `td` elements for the header row of
the table. These will apply slightly different styles.

Table captions should be placed before the first row inside of the `table`
element using `<caption>Title of table</caption>`.

### Column-Formatting

If you would like the page content to be split into columns, there's a special
element you can wrap your content in: `<div style="columns: 2"></div>`. This
could be implemented like so:

```
<div style="columns: 2">
	<p>
		...
	</p>
	<p>
		...
	</p>
</div>
```

### Page Breaks

You can place a page break anywhere by simply adding the following element:

```
<div class="page-break"></div>
```

### Footnotes

Footnotes can be inserted anywhere using the following snippet in your
paragraph text:

```
<span class="fn">Footnote text</span>
```
These will automatically number themselves and place the note at the bottom of
the appropriate page