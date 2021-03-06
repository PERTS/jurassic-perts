Jurassic PERTS
==========

Jurassic PERTS is a tool for generating PDF files from HTML using standard
styling used by the PERTS organization. It is available for use at
http://jurassic-perts.appspot.com. Please contact the PERTS team for an access
code to use non-test documents.

## Option 1. Web Interface

The easiest way to use the PDF generator is just to use the form available
online at 
[http://jurassic-perts.appspot.com](http://jurassic-perts.appspot.com).
Simply upload your own HTML file (just one at a time) and set the appropriate
settings. Your PDF will download in the same way any other document would after
a short delay.

#### Note on API Key:

API Keys for the web application are setup through SecretValues in the API.
In order to use an API key to create a non-test document, you'll need to fetch
an access code from a PERTS team member. (Alternatively, you could also use
your own API key and run locally, see below.)

________________

## Option 2. Running Locally

For the more savvy user, running PDF generator on your on computer offers much
more functionality and flexibility. Benefits include: converting multiple
documents with a single command, faster processing, and better error reporting.

Follow the steps below to perform PDF generation on your computer (Mac).
Instructions may vary for Windows devices.

1. Put the html files you want to convert in subdirectory `inbox`
2. Then from the root directory run:

```
python generate.py your_api_key
```
Note: `your_api_key` is a valid DocRaptor API Key. If you are on the PERTS team
you can obtain a key from [this document](https://docs.google.com/document/d/1IGn6A5pB_5YCltbI9r1CGCvWRFG1Hcna3ya67ulZeLA/). You can also set up an
account of your own through [DocRaptor](https://docraptor.com/signup).

3. PDF files will be generated in a `outbox` subdirectory.

### Setup

Please run the following command at add necessary python libraries to your
machine. You may need to install `pip` if you have not already done so.

```
sudo pip install lxml 3.7.1
```

### Production v. Testing

By default PDF files are generated in 'testing' mode with DocRaptor. These are
free for PERTS and do not count against the quota we pay for each month.

To make PDFs for production (something you would want to send to schools) you
will need to add a `production` flag to the python command:

```
python generate.py your_api_key --production
```

### Pre-defined Styles

To make your PDF Generation especially simple, we provide a set of styles that
will help your documents conform to PERTS style guidelines. This includes a
cover page, headers, footers, and much more.

To use our styles, you don't need to do a thing. However, if you'd like to
ignore them and use your own embedded styles, you can run the python command:

```
python generate.py your_api_key --ignore-styles
```

### Table of Contents

To make your life _even easier_ PDF Generator is able to automatically generate
a Table of Contents (TOC) for your document.

```
python generate.py your_api_key --toc
```

You can learn more about how the Table of Contents is created further in this
document. Please read this over, especially if your documents are not coming
out the way you'd expect.

________________

## Notes on Styling

DocRaptor provides an API to render PDF document from HTML using Prince XML
software.

### DocRaptor

To get better acquianted with DocRaptor and their API you can take a look at
[their documentation](http://docraptor.com/).

### Prince XML

Prince XML is a powerful library for creating PDF documents. They provide a
wide variety of incredibly useful styles such as column formatting and
footnotes. Learn more about Prince in their
[guide](https://www.princexml.com/doc/). Settings are managed 

## Components

A variety of basic styles are covered by the CSS rules in 
`/templates/reports/_styles.html`. These are injected in any file by default
but can be turned off if you'd like to use your own.

An example of html input: [example.html](../master/examples/example.html)

And corresponding pdf output: [example.pdf](../master/examples/example.pdf)

### Cover page

```html
<div id="cover_page">
  <img src="https://s3.amazonaws.com/PERTS/images/perts-logo.png" />
  <h1 class="title">
    Example Document
  </h1>
  <h3>
    July 28, 2016
  </h3>
</div>
```

### Table of Contents

The Table of Contents will automatically generate page numbers if properly set
up. Use a `div` with a `toc` id. (`<div id="toc">...</div>`)

By convention, the first level of headers should match up with `h1` tags in the
document, the second level should match with `h2` and so on.

The final result might look something like:
```html
<!-- TOC -->
<div id="toc">
  <li>
    <a href="#section-1">Section 1</a>
  </li>
  <li>
    <a href="#section-2">Section 2</a>
    <ol>
      <li>
        <a href="#level-two-header">
          Level Two Header
        </a> 
      </li>
      <li>
        <a href="#exploring-duo-columns">
          Exploring Duo Columns
        </a> 
      </li>
    </ol>
  </li>
  <li>
    <a href="#section-3">Section 3</a>
  </li>
</div>
```

*Important:* Be sure to include `id` attributes for each of your section
headers like so:
```html
<h1 id="section-2">
  Section 2
</h1>
```
This ensures that the Table of Contents will link to pages within the PDF.
These should match the `href`s you specify in the `a` elements in your TOC.

### Auto-Generated TOC

A table of contents can be generated automatically following a specific set of
rules. The TOC will resemble the example code above and use the following:

1. The HTML Parser searches for and finds all `h2` `h2` and `h3` elements in
your HTML.
2. For each header, an `id` is assigned to it by parameterizing its text. For
example, "Header 1" would become header-1 to be url safe.
3. A table of contents is constructed by embedding the header names in order.
Any lesser headers will appear within any leading ones.
4. The table of contents is inserted into the document in a place of the
following line of HTML. This allows you to control the position.
```html
<div id="toc"></div>
```
*Note: Automatic generation will fail if the html above is missing.

### Figures

Figures can be inserted anywhere in the document using a `figure` element.

Example:
```html
<figure>
  <img src="https://..." />
  <figcaption>Figure caption goes here</figcaption>
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

Tables can easily be inserted using the PERTS colors (various shades of blue)
using the following syntax:
```html
<table class="xtable">
  <caption>Title of the table</caption>
  <tr>
    <th>Header 1</th>
    <th>Header 2</th>
    <th>Header 3</th>
    <th>Header 4</th>
  </tr>
  <tr>
    <td>Row 1</td>
    <td>Value 1</td>
    <td>Value 2</td>
    <td>Value 3</td>
  </tr>
  <tr>
    <td>Row 2</td>
    <td>Value 1</td>
    <td>Value 2</td>
    <td>Value 3</td>
  </tr>
  <tr>
    <td>Row 3</td>
    <td>Value 1</td>
    <td>Value 2</td>
    <td>Value 3</td>
  </tr>
</table>
```

Be sure to use `th` elements instead of `td` elements for the header row of
the table. These will apply slightly different styles.

Table captions should be placed before the first row inside of the `table`
element using `<caption>Title of table</caption>`.

*@todo*: Create other color combinations if desired.

### Column-Formatting

If you would like the page content to be split into columns, there's a special
element you can wrap your content in: `<div style="columns: 2"></div>`. This
could be implemented like so:

```html
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

```html
<div class="page-break"></div>
```

### Footnotes

Footnotes can be inserted anywhere using the following snippet in your
paragraph text:

```html
<span class="fn">Footnote text</span>
```
These will automatically number themselves and place the note at the bottom of
the appropriate page.  The full content might look like this:
```html
<p>
	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris in sapien
	a elit commodo tempus. Nam dignissim, augue sit amet vulputate
	sollicitudin<span class="fn">nibh ligula ultricies nibh</span> ut fermentum 
	urna massa eget tortor. Phasellus elementum enim vel odio vulputate, quis
	finibus lorem fermentum. Donec nisi massa, commodo ac malesuada at, maximus
	in odio. Sed iaculis magna ac dignissim rhoncus. Nulla pretium orci viverra
	risus volutpat congue. In euismod maximus ligula non pharetra.
</p>
```

## Continued Work

Jurassic PERTS can be considered a _beta_ product! Please let us know how we
can improve it to be easier to use or cover more use-cases.
