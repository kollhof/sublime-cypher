import sublime
import sublime_plugin


import urllib2
import json


def item_to_str(item):
    if isinstance(item, dict):
        data = json.dumps(item['data'])
        id_ = item['self'].rsplit('/', 1)[1]

        if 'type' in item:
            return "[%s:%s %s]" % (
                id_, item['type'], data)
        else:
            return "(%s %s)" % (id_, data)
    else:
        return str(item)


def print_table(headers, items):
    column_widths = {}
    rows = []

    for col_idx, header in enumerate(headers):
        column_widths[col_idx] = len(header)

    for row in items:
        row = tuple(item_to_str(item) for item in row)
        for col_idx, data in enumerate(row):
            col_width = column_widths[col_idx]
            column_widths[col_idx] = max(col_width, len(data))
        rows.append(row)

    headers = [c.center(column_widths[i]) for i, c in enumerate(headers)]
    lines = ['-' * column_widths[i] for i, c in enumerate(headers)]

    lines = '+-' + '-+-'.join(lines) + '-+'

    print lines
    print '| ' + ' | '.join(headers) + ' |'
    print lines

    for row in rows:
        fields = [c.ljust(column_widths[i]) for i, c in enumerate(row)]
        print '| ' + ' | '.join(fields) + ' |'

    print lines

    print "%d items returned" % len(rows)


def print_error(file_name, query, err):
    try:
        ex = err['exception']
        msg = err['message']
        print '------------'
        print msg
        print '==============='
        if ex == 'SyntaxException':
            try:
                _, match, col = msg.rsplit('\n', 2)
                col = col.index('^')
                match = match.strip('"')
                line_num = 0
                for line_num, lne in enumerate(query.splitlines()):
                    if match in lne:
                        break

                line_num += 1
                msg = 'File "%s:%s:%s": %s' % (file_name, line_num, col, msg)
                print msg
                return line_num, col
            except Exception, e:
                pass

        msg = 'File "%s"\n%s: %s' % (file_name, ex, msg)
    except Exception as e:
        msg = e
        from traceback import format_exc
        msg = format_exc()

    print msg


def cypher(query, **args):

    data = {
        "query": query,
        "params": args
    }

    data = json.dumps(data)

    req = urllib2.Request(
        url="http://localhost:7474/db/data/cypher",
        data=data)

    req.add_header('Accept', 'application/json')
    req.add_header('Content-Type', 'application/json')

    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError as err:
        if err.code == 400:
            err = json.loads(err.read())
            return print_error('', query, err)
        else:
            print err

        return
    else:
        resp = json.loads(resp.read())
        columns = resp['columns']
        rows = resp['data']
        print_table(columns, rows)


class CypherCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()

        for sel in sels:
            if sel.size() == 0:
                sel = sublime.Region(0, self.view.size())

            query = self.view.substr(sel)
            cypher(query)
