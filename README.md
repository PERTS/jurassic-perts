Jurassic PERTS
==========

Jurassic PERTS is a tool for generating PDF files from HTML using standard
styling used by the PERTS organization. It is available for use at
http://jurassic-perts.appspot.com. Please contact the PERTS team for an access
code to use non-test documents.

## About Styling

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
<h2 id="section-2">
  Section 2
</h2>
```
This ensures that the Table of Contents will link to pages within the PDF.
These should match the `href`s you specify in the `a` elements in your TOC.

*Note*: We may explore auto-generation of the TOC in future iterations if that
would be useful.

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