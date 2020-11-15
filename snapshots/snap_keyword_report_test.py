# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_generate_table 1'] = '''<html>
  <head>
    <link href="styling.css" rel="stylesheet">
  </head>
  <body>
    <h1>
      Keyword extraction
    </h1>
    <h2>
      Documents scanned:
    </h2>
    <ol>
      <li>
        <a href="doc">
          doc
        </a>
      </li>
    </ol>
    <h2>
      Keyword list
    </h2>
    <table class="data-table">
      <tbody>
        <tr>
          <th>
            Word stem (Words)
          </th>
          <th>
            Total sentence occurrences
          </th>
          <th>
            Documents
          </th>
          <th>
            Sentences containing the words
          </th>
        </tr>
        <tr>
          <td>
            <span class="highlight">
              test
            </span>
            (test)
          </td>
          <td>
            1
          </td>
          <td>
            <ul class="doclist">
              <li>
                doc
              </li>
            </ul>
          </td>
          <td>
            <h3>
              doc
            </h3>
            <p class="sentence">
              this is a
              <span class="highlight">
                test
              </span>
              about testing functions.
            </p>
          </td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
'''
