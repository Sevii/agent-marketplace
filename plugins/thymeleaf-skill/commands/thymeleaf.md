# Thymeleaf 3.1 Skill

You are an expert in Thymeleaf, the modern server-side Java template engine. Use this reference when helping users write, debug, or review Thymeleaf templates. Always produce idiomatic Thymeleaf that works as a natural template (viewable as static HTML in a browser).

---

## Core Principles

- Thymeleaf templates are valid HTML. Static prototype content is replaced at runtime by `th:*` attributes.
- Always provide realistic placeholder content inside tags so the template is useful as a static prototype.
- Prefer `th:text` (HTML-escaped) over `th:utext` (unescaped) unless raw HTML output is explicitly needed.
- Use the HTML5-friendly `data-th-*` syntax when strict HTML5 validation is required.

---

## Template Modes

| Mode       | Use case                                    |
|------------|---------------------------------------------|
| HTML       | Web pages (HTML5, XHTML) - the default      |
| XML        | Strict XML documents                        |
| TEXT       | Plain text (emails, docs)                   |
| JAVASCRIPT | JavaScript files with model data            |
| CSS        | CSS files with model data                   |
| RAW        | Untouched resource passthrough              |

---

## Standard Expression Syntax

### Variable Expressions `${...}`

Access context variables via OGNL (or SpEL in Spring):

```html
<p th:text="${user.name}">John Doe</p>
<p th:text="${user.address.city}">Springfield</p>
<p th:text="${users[0].name}">First User</p>
<p th:text="${countriesByCode['US']}">United States</p>
<p th:text="${user.getFormattedName()}">John Doe</p>
```

### Selection Variable Expressions `*{...}`

Evaluate against a previously selected object (`th:object`):

```html
<div th:object="${session.user}">
  <p>Name: <span th:text="*{firstName}">Sebastian</span></p>
  <p>Surname: <span th:text="*{lastName}">Pepper</span></p>
</div>
```

Without `th:object`, `*{...}` is equivalent to `${...}`.

### Message Expressions `#{...}`

Internationalized messages from `.properties` files:

```html
<p th:text="#{home.welcome}">Welcome!</p>
<p th:text="#{home.welcome(${session.user.name})}">Welcome, User!</p>
```

Property files: `messages.properties` (default), `messages_en.properties`, `messages_es.properties`, etc.

### Link URL Expressions `@{...}`

Build URLs with automatic context path prefixing and parameter encoding:

```html
<!-- Absolute -->
<a th:href="@{https://example.com/path}">Link</a>

<!-- Context-relative (prepends app context path) -->
<a th:href="@{/order/details(orderId=${o.id})}">View</a>

<!-- Path variables -->
<a th:href="@{/order/{orderId}/details(orderId=${o.id})}">View</a>

<!-- Multiple parameters -->
<a th:href="@{/order/process(execId=${execId},execType='FAST')}">Process</a>

<!-- Server-relative (bypasses app context) -->
<a th:href="@{~/billing/processInvoice}">Invoice</a>

<!-- Protocol-relative -->
<script th:src="@{//cdn.example.com/lib.js}"></script>
```

### Fragment Expressions `~{...}`

Reference reusable template fragments:

```html
<div th:insert="~{fragments/header :: nav}">...</div>
<div th:replace="~{footer :: copy}">...</div>
```

Formats:
- `~{templatename :: selector}` - fragment from another template
- `~{templatename}` - entire template
- `~{:: selector}` or `~{this :: selector}` - fragment in same template

---

## Literals and Operations

### Literals

```html
<!-- Text (single quotes, escape with \') -->
<span th:text="'Hello, World!'">text</span>

<!-- Numbers -->
<span th:text="42">0</span>
<span th:text="3.14">0.0</span>

<!-- Booleans -->
<span th:if="${user.active} == true">Active</span>

<!-- Null -->
<span th:if="${value} == null">No value</span>

<!-- Literal tokens (no quotes needed for simple identifiers) -->
<div th:class="content">...</div>
```

### String Concatenation and Literal Substitution

```html
<!-- Concatenation with + -->
<span th:text="'Hello, ' + ${user.name} + '!'">Hello, User!</span>

<!-- Literal substitution with |...| (preferred) -->
<span th:text="|Welcome to our app, ${user.name}!|">Welcome, User!</span>
```

### Arithmetic

`+`, `-`, `*`, `/`, `%` (or `mod`)

### Comparisons

- Symbols: `>`, `<`, `>=`, `<=` (use XML-escaped `&gt;` etc. in attributes)
- Text aliases (preferred): `gt`, `lt`, `ge`, `le`
- Equality: `==`, `!=` (or `eq`, `ne`/`neq`)

### Boolean Operators

`and`, `or`, `!` (or `not`)

### Conditional (Ternary) and Default (Elvis)

```html
<!-- If-then-else -->
<span th:class="${row.even} ? 'even' : 'odd'">row</span>

<!-- Elvis operator (default for null) -->
<span th:text="${user.name} ?: 'Anonymous'">name</span>

<!-- No-op token _ (keep prototype content) -->
<span th:text="${user.name} ?: _">prototype name</span>
```

---

## Expression Utility Objects

Use `#objectName` inside expressions:

| Object         | Purpose                                |
|----------------|----------------------------------------|
| `#strings`     | String utilities (isEmpty, contains, etc.) |
| `#numbers`     | Number formatting                      |
| `#dates`       | java.util.Date formatting              |
| `#calendars`   | java.util.Calendar formatting          |
| `#temporals`   | java.time (JDK 8+) formatting         |
| `#lists`       | List utilities                         |
| `#sets`        | Set utilities                          |
| `#maps`        | Map utilities                          |
| `#arrays`      | Array utilities                        |
| `#objects`     | General object utilities               |
| `#bools`       | Boolean evaluation                     |
| `#uris`        | URI/URL escaping                       |
| `#messages`    | Externalized messages                  |
| `#conversions` | Conversion service                     |
| `#execInfo`    | Template execution info                |
| `#aggregates`  | Aggregation (sum, avg)                 |
| `#ids`         | ID generation for repeated elements    |
| `#locale`      | Current locale                         |
| `#ctx`         | Context object                         |

Examples:

```html
<p th:text="${#strings.isEmpty(name)}">false</p>
<p th:text="${#strings.toUpperCase(name)}">NAME</p>
<p th:text="${#lists.size(items)}">0</p>
<p th:text="${#dates.format(date, 'dd/MMM/yyyy')}">01/Jan/2025</p>
<p th:text="${#temporals.format(localDate, 'yyyy-MM-dd')}">2025-01-01</p>
<p th:text="${#numbers.formatDecimal(price, 1, 2)}">0.00</p>
```

---

## Setting Attribute Values

### Specific Attributes

Use `th:attributename` for any HTML attribute:

```html
<input type="text" th:value="${user.name}" value="prototype" />
<a th:href="@{/products}">Products</a>
<form th:action="@{/save}" th:method="post">
<img th:src="@{/images/logo.png}" th:alt="#{logo.alt}" src="logo.png" alt="Logo" />
<div th:id="${'row-' + item.id}" id="row-1">...</div>
<input th:class="${hasError} ? 'error' : 'valid'" class="valid" />
```

### Generic Attribute Setting `th:attr`

```html
<img th:attr="src=@{/img/logo.png},alt=#{logo}" />
```

### Appending and Prepending

```html
<div class="base" th:classappend="${isActive} ? 'active'">...</div>
<div th:styleappend="'color:' + ${color}">...</div>
<input th:attrappend="class=${' ' + extraClass}" />
```

### Boolean Attributes

Rendered or omitted based on truthiness:

```html
<input type="checkbox" th:checked="${user.active}" />
<input type="text" th:disabled="${isReadOnly}" />
<input type="text" th:readonly="${isReadOnly}" />
<select th:multiple="${allowMulti}">...</select>
<option th:selected="${opt.id == selected}">...</option>
```

---

## Iteration

### `th:each`

```html
<tr th:each="product : ${products}">
  <td th:text="${product.name}">Product Name</td>
  <td th:text="${product.price}">0.00</td>
</tr>
```

Works with: `Iterable`, `Map` (entries), `Stream`, arrays, `Enumeration`, `Iterator`, and single objects.

### Iteration Status Variable

Implicitly named `${varStat}` or explicitly declared:

```html
<tr th:each="product, stat : ${products}"
    th:class="${stat.odd} ? 'odd'">
  <td th:text="${stat.index}">0</td>
  <td th:text="${product.name}">Name</td>
</tr>
```

| Property   | Description                   |
|------------|-------------------------------|
| `index`    | 0-based index                 |
| `count`    | 1-based count                 |
| `size`     | Total elements                |
| `current`  | Current element               |
| `even`     | true if even (0-based)        |
| `odd`      | true if odd (0-based)         |
| `first`    | true if first element         |
| `last`     | true if last element          |

---

## Conditional Evaluation

### `th:if` and `th:unless`

```html
<div th:if="${not #lists.isEmpty(products)}">
  <p>We have products!</p>
</div>

<p th:unless="${user.active}">Account is inactive.</p>
```

Truthiness rules: `null` is false; `false`, `0`, `"false"`, `"off"`, `"no"` are false; everything else is true.

### `th:switch` / `th:case`

```html
<div th:switch="${user.role}">
  <p th:case="'admin'">Administrator</p>
  <p th:case="'manager'">Manager</p>
  <p th:case="*">Other role</p>
</div>
```

`th:case="*"` is the default case. Only the first matching case renders.

---

## Template Layout and Fragments

### Defining Fragments

```html
<!-- In fragments/header.html -->
<nav th:fragment="topnav">
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>
```

### Including Fragments

```html
<!-- th:insert - inserts fragment INSIDE the host tag -->
<div th:insert="~{fragments/header :: topnav}"></div>
<!-- Result: <div><nav>...</nav></div> -->

<!-- th:replace - REPLACES the host tag with the fragment -->
<div th:replace="~{fragments/header :: topnav}"></div>
<!-- Result: <nav>...</nav> -->
```

### Parameterized Fragments

```html
<!-- Definition -->
<div th:fragment="alert(type, message)">
  <div th:class="|alert alert-${type}|" th:text="${message}">Alert text</div>
</div>

<!-- Call with positional args -->
<div th:replace="~{components :: alert('danger', ${errorMsg})}"></div>

<!-- Call with named args (order-independent) -->
<div th:replace="~{components :: alert(message=${msg}, type='info')}"></div>
```

### Layout Composition with Fragment Parameters

```html
<!-- layout/base.html -->
<html>
<head th:fragment="common_header(title, links)">
  <title th:replace="${title}">Default Title</title>
  <link rel="stylesheet" th:href="@{/css/main.css}" />
  <th:block th:replace="${links}" />
</head>
<body>
  <div th:replace="${content}">Default content</div>
</body>
</html>

<!-- page.html -->
<head th:replace="~{layout/base :: common_header(~{:: title}, ~{:: link})}">
  <title>My Page</title>
  <link rel="stylesheet" th:href="@{/css/page.css}" />
</head>
```

### Empty Fragment and No-Op Token

```html
<!-- Pass empty fragment (renders nothing) -->
<div th:replace="~{layout :: section(~{})}"></div>

<!-- No-op: keep default content from the fragment definition -->
<div th:replace="~{layout :: section(_)}"></div>
```

### Fragment Assertions

```html
<header th:fragment="contentheader(title)"
        th:assert="${!#strings.isEmpty(title)}">
  <h1 th:text="${title}">Title</h1>
</header>
```

### Removing Elements `th:remove`

```html
<table>
  <tr th:remove="all"><!-- prototype-only row removed at runtime --></tr>
</table>
```

Values: `all` (tag + children), `body` (children only), `tag` (tag only, keep children), `all-but-first` (all children except first), `none` (do nothing).

---

## Local Variables `th:with`

```html
<div th:with="fullName=${user.firstName + ' ' + user.lastName}">
  <p th:text="${fullName}">Full Name</p>
</div>

<!-- Multiple variables -->
<div th:with="total=${price * qty}, tax=${total * 0.1}">
  <p th:text="|Total: ${total}, Tax: ${tax}|">Total: 0, Tax: 0</p>
</div>
```

---

## Inlining

### Text Inlining

Output expressions directly in text content:

```html
<!-- Escaped output -->
<p>Hello, [[${user.name}]]!</p>

<!-- Unescaped output -->
<p>[(${htmlContent})]</p>

<!-- Disable inlining in a block -->
<div th:inline="none">
  <p>This shows literal [[${not.processed}]]</p>
</div>
```

### JavaScript Inlining

```html
<script th:inline="javascript">
  var user = [[${user}]];
  var username = [[${user.name}]];

  /* Natural template with fallback for static viewing */
  var count = /*[[${itemCount}]]*/ 0;
  var items = /*[[${itemList}]]*/ ['placeholder'];
</script>
```

Thymeleaf serializes objects to JSON and properly escapes strings.

### CSS Inlining

```html
<style th:inline="css">
  .main {
    background-color: /*[[${bgColor}]]*/ #f0f0f0;
  }
</style>
```

---

## The `th:block` Element

A synthetic container that disappears after processing:

```html
<th:block th:each="user : ${users}">
  <tr>
    <td th:text="${user.name}">Name</td>
  </tr>
  <tr>
    <td th:text="${user.email}">email@example.com</td>
  </tr>
</th:block>
```

---

## Comments

```html
<!-- Standard HTML comment (visible in output) -->
<!-- This comment appears in rendered HTML -->

<!-- Parser-level comment (removed entirely) -->
<!--/* This is completely removed during processing */-->

<!-- Prototype-only comment (shown in static view, removed at runtime) -->
<!--/*/
  <p>Only visible when viewing template as static HTML</p>
/*/-->
```

---

## Attribute Precedence

When multiple `th:*` attributes are on one element, they execute in this order:

1. `th:insert`, `th:replace` (fragment inclusion)
2. `th:each` (iteration)
3. `th:if`, `th:unless`, `th:switch`, `th:case` (conditionals)
4. `th:with` (local variable definition)
5. `th:attr`, `th:attrappend`, `th:attrprepend` (general attribute modification)
6. `th:value`, `th:href`, `th:src`, etc. (specific attribute setting)
7. `th:text`, `th:utext` (text content)
8. `th:fragment`, `th:remove` (fragment specification / removal)

---

## Data Conversion with Double Braces

Apply the registered conversion service (e.g., Spring's):

```html
<td th:text="${{user.lastAccessDate}}">Jan 1, 2025</td>
```

---

## Preprocessing `__...__`

Evaluate inner expressions first to build dynamic outer expressions:

```html
<p th:text="${__#{article.text('textVar')}__}">...</p>
```

---

## Form Handling (Spring Integration)

### Form Binding

```html
<form th:action="@{/users/save}" th:object="${userForm}" method="post">
  <input type="text" th:field="*{username}" />
  <input type="email" th:field="*{email}" />
  <textarea th:field="*{bio}"></textarea>

  <!-- Validation errors -->
  <span th:if="${#fields.hasErrors('username')}"
        th:errors="*{username}">Username error</span>

  <!-- Global errors -->
  <div th:if="${#fields.hasGlobalErrors()}">
    <p th:each="err : ${#fields.globalErrors()}" th:text="${err}">Error</p>
  </div>

  <button type="submit">Save</button>
</form>
```

### Select / Option

```html
<select th:field="*{country}">
  <option value="">-- Select --</option>
  <option th:each="c : ${countries}"
          th:value="${c.code}"
          th:text="${c.name}">Country</option>
</select>
```

### Checkboxes and Radio Buttons

```html
<!-- Single checkbox (boolean) -->
<input type="checkbox" th:field="*{active}" />

<!-- Multi checkbox -->
<div th:each="role : ${allRoles}">
  <input type="checkbox" th:field="*{roles}" th:value="${role}" />
  <label th:text="${role}">Role</label>
</div>

<!-- Radio buttons -->
<div th:each="type : ${types}">
  <input type="radio" th:field="*{type}" th:value="${type}" />
  <label th:text="${type}">Type</label>
</div>
```

---

## Common Patterns

### Pagination

```html
<nav>
  <ul>
    <li th:each="pageNum : ${#numbers.sequence(1, totalPages)}"
        th:class="${pageNum == currentPage} ? 'active'">
      <a th:href="@{/items(page=${pageNum})}" th:text="${pageNum}">1</a>
    </li>
  </ul>
</nav>
```

### Conditional CSS Classes

```html
<div th:classappend="${hasError} ? 'has-error'">
  <input th:classappend="${field.invalid} ? 'is-invalid'" />
</div>
```

### Empty State

```html
<table>
  <tr th:each="item : ${items}">
    <td th:text="${item.name}">Item</td>
  </tr>
  <tr th:if="${#lists.isEmpty(items)}">
    <td colspan="3">No items found.</td>
  </tr>
</table>
```

### Date Formatting

```html
<span th:text="${#temporals.format(event.date, 'MMMM d, yyyy')}">January 1, 2025</span>
<span th:text="${#dates.format(legacyDate, 'yyyy-MM-dd HH:mm')}">2025-01-01 12:00</span>
```

### Number Formatting

```html
<span th:text="${#numbers.formatDecimal(price, 1, 2)}">0.00</span>
<span th:text="${#numbers.formatCurrency(price)}">$0.00</span>
<span th:text="${#numbers.formatPercent(ratio, 1, 2)}">0.00%</span>
```

### Security (Spring Security dialect)

```html
<div sec:authorize="hasRole('ADMIN')">Admin-only content</div>
<span sec:authentication="name">username</span>
```

---

## Best Practices

1. **Natural templates**: Always include realistic static content as fallback so templates work in a browser without the server.
2. **Escape by default**: Use `th:text` (escaped). Only use `th:utext` when you explicitly trust the HTML content.
3. **Fragment reuse**: Extract repeated markup (headers, footers, navs) into fragment files under a `fragments/` or `layout/` directory.
4. **Literal substitution**: Prefer `|...|` syntax over string concatenation with `+` for readability.
5. **Utility objects**: Use `#strings`, `#lists`, `#temporals` etc. instead of writing verbose OGNL/SpEL.
6. **Avoid `th:attr`**: Use specific `th:*` attributes (`th:href`, `th:src`, `th:value`) instead of the generic `th:attr` when possible.
7. **Use `th:block`**: When you need to apply `th:each` or `th:if` around multiple sibling elements without adding a wrapper tag.
8. **Decoupled template logic**: For pure-HTML templates consumed by designers, place Thymeleaf attributes in separate `.th.xml` files.
9. **URL expressions**: Always use `@{...}` for URLs to get automatic context path handling and parameter encoding.
10. **Form binding**: Use `th:field` with `th:object` for Spring form binding rather than manually setting `name`, `value`, and `id` attributes.
