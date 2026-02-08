# Thymeleaf Skill

A Claude Code skill plugin that provides comprehensive Thymeleaf 3.1 template engine reference and guidance.

## What It Does

When invoked, this skill gives Claude Code deep knowledge of Thymeleaf's template syntax, expression language, and best practices. It covers:

- **Standard Expression Syntax** - Variable (`${}`), selection (`*{}`), message (`#{}`), URL (`@{}`), and fragment (`~{}`) expressions
- **Attribute Setting** - Specific attributes (`th:href`, `th:src`, etc.), boolean attributes, class/style appending
- **Iteration** - `th:each` with status variables, supported collection types
- **Conditionals** - `th:if`, `th:unless`, `th:switch`/`th:case`
- **Template Layout** - Fragment definition, `th:insert`, `th:replace`, parameterized fragments, layout composition
- **Inlining** - Text, JavaScript, and CSS inlining with natural template fallbacks
- **Form Handling** - Spring form binding with `th:field`, `th:object`, validation errors
- **Utility Objects** - `#strings`, `#numbers`, `#dates`, `#temporals`, `#lists`, and more
- **Common Patterns** - Pagination, conditional CSS, empty states, date/number formatting

## Installation

Add this plugin to your Claude Code configuration to make the `/thymeleaf` skill command available in your projects.

## Usage

Invoke the skill when working on Thymeleaf templates:

```
/thymeleaf
```

This loads the full Thymeleaf reference into context so Claude Code can provide accurate, idiomatic template assistance.

## Source

Based on the official Thymeleaf 3.1 documentation: https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html
