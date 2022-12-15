# Datasets

This directory contains the datasets used in our project.

> **Note:**\
> The raw datasets can be found in the [`raw`](raw) directory.

## Merged Dataset

The merged dataset is the result of merging the raw datasets into a single dataset.
This includes performing some preprocessing steps, such as normalization, removing duplicates, and catching data integrity issues.

### Duplicate Example

Here is an example of a duplicate sample.
The URL `http://www.0068555.com/cl/js/jquery-ui-1.8.21.custom.min.js?v=ver31.32` and corresponding label are duplicated across the dataset.
This example can be found in the [t4-urls-raw.csv](t4-urls-raw.csv).
This duplication does not come from the merging of multiple datasets, but instead from the
raw [urls-manu-siddhartha.csv](raw/urls-manu-siddhartha.csv) dataset.

This is an oversight from the original dataset creator, and provides an example of how raw our datasets are.
We counted duplicate URLs across our merged dataset of `726,875` total URLs.
We found `10,271` URLs being duplicated, with `19,303` duplicates, not counting the first true URL.
This might seem like a small percentage of the total dataset (`2.65%`), but it is still a significant amount of data.
To ensure that we are not introducing any bias into our dataset, we remove these duplicates.

|        | url                                                                        | label |
|:-------|:---------------------------------------------------------------------------|------:|
| ...    | ...                                                                        |   ... |
| 432659 | `http://www.0068555.com/cl/js/jquery-ui-1.8.21.custom.min.js?v=ver31.32,1` |     1 |
| 432660 | `http://www.0068555.com/cl/js/jquery-ui-1.8.21.custom.min.js?v=ver31.32,1` |     1 |
| 432661 | `http://www.0068555.com/cl/js/jquery-ui-1.8.21.custom.min.js?v=ver31.32,1` |     1 |
| 432662 | `http://www.0068555.com/cl/js/jquery-ui-1.8.21.custom.min.js?v=ver31.32,1` |     1 |
| 432663 | `http://www.0068555.com/cl/js/jquery-ui-1.8.21.custom.min.js?v=ver31.32,1` |     1 |
| ...    | ...                                                                        |   ... |

### Conflicting Example

Here is an example of a conflicting sample created while merging the datasets.
The URL `pastehtml.com/view/b46s81spf.html` is found multiple times in the merged dataset, but with different labels.
This example can be found in the [t4-urls-raw.csv](t4-urls-raw.csv).

This is created because the URL is present in multiple of the raw datasets we use, but given different labels.
This is a possible sign of data poisoning, and we have seen this with a few other URLs.
In this example, it is most likely because the `pastehtml.com` domain can be used by many individual to host their own content.
The path `b46s81spf` likely expires for one individual, and is then recycled to be used by another individual.
Depending on when the raw datasets were created they may both be accurate.

We found `58` URLs with conflicting labels, each with only a single conflict for a total of `116` conflicting samples.
While this is only `0.015`% of the total dataset, we do not want to introduce any possible bias or data poisoning.
We do not choose a "winner" label, but instead remove all `116` conflicting samples to ensure data integrity.

|            | url                                    | label |
|:-----------|:---------------------------------------|------:|
| ...        | ...                                    |   ... |
| 42764      | `sites.google.com/site/habbomoedasgt/` |     1 |
| **42765**  | `pastehtml.com/view/b46s81spf.html`    |     1 |
| 42766      | `sites.google.com/site/haabbohoteell/` |     1 |
| ...        | ...                                    |   ... |
| 640437     | `pastehtml.com/view/b4mb3nlq6.html`    |     0 |
| **640438** | `pastehtml.com/view/b46s81spf.html`    |     0 |
| 640439     | `pastehtml.com/view/b4hmu2v5o.html`    |     0 |
| ...        | ...                                    |   ... |