# Pull Request

## 📝 Description

Brief description of the changes in this PR.

## 🎯 Type of Change

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🧪 Test improvements
- [ ] 🔧 Refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] 🔒 Security fix

## 🧪 Testing

Describe the tests you ran to verify your changes:

- [ ] Unit tests pass (`uv run pytest`)
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Code coverage maintained/improved

**Test Environment:**
- OS: 
- Python version: 
- Dependencies: 

## 📋 Checklist

### Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My code passes all quality checks (`uv run black --check . && uv run ruff check . && uv run mypy wise_mise/`)

### Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested the MCP integration manually

### Documentation
- [ ] I have made corresponding changes to the documentation
- [ ] I have updated the changelog if this is a user-facing change
- [ ] I have added docstrings to new functions/classes
- [ ] Examples in the README still work with my changes

### Dependencies
- [ ] I have not introduced any new dependencies unnecessarily
- [ ] Any new dependencies are properly declared in pyproject.toml
- [ ] Dependencies are compatible with the minimum Python version (3.10+)

## 🔗 Related Issues

Fixes #(issue_number)
Closes #(issue_number)
Related to #(issue_number)

## 🧠 Domain Expertise

If this PR adds or modifies domain experts:

- [ ] I have tested the expert with real project examples
- [ ] The expert follows the established patterns
- [ ] I have documented the technologies/frameworks supported
- [ ] Error handling is appropriate for edge cases

## 💡 MCP Integration

If this PR affects MCP tools:

- [ ] Tool descriptions are clear and helpful
- [ ] Request/response models are properly typed
- [ ] Tools work correctly with MCP clients
- [ ] Error messages are user-friendly

## 🎨 User Experience

- [ ] Changes improve or maintain good user experience
- [ ] Error messages are helpful and actionable  
- [ ] Performance impact has been considered
- [ ] Backward compatibility is maintained (or breaking changes are documented)

## 📸 Screenshots/Examples

If applicable, add screenshots or code examples showing the changes:

```python
# Example usage of new feature
```

## 🚀 Additional Notes

Any additional information, deployment notes, or special considerations for reviewers.

---

**Reviewer Notes:**
- [ ] Code review completed
- [ ] Testing strategy approved
- [ ] Documentation is adequate
- [ ] Ready for merge