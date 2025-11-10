# Pull Request

## Description
Brief description of what this PR does and why.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Workflow configuration change
- [ ] Test/CI improvement

## Changes Made
- [ ] Modified N8N workflow nodes
- [ ] Updated documentation
- [ ] Added new test cases
- [ ] Updated environment configuration
- [ ] Fixed security issue

## Testing
- [ ] I have tested this workflow end-to-end
- [ ] All existing tests pass
- [ ] I have added tests for new functionality
- [ ] The workflow JSON validates successfully
- [ ] I have tested with sample data

### Test Results
```
# Paste test results or describe manual testing performed
$ ./test-requests.sh
✅ Start collection: 200 OK
✅ Submit offers: 200 OK
✅ Get summary: 5 offers returned
```

## Configuration Changes
- [ ] No configuration changes required
- [ ] Updated .env.example with new variables
- [ ] Updated CONTRIBUTING.md with new setup steps
- [ ] Added new dependencies or requirements

### New Environment Variables
```
# List any new environment variables added
NEW_VARIABLE=example_value
ANOTHER_VARIABLE=another_example
```

## Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes (describe below)

### Breaking Change Description
If this introduces breaking changes, describe:
1. What will stop working
2. How users should migrate
3. Any deprecation notices

## Security Considerations
- [ ] No security impact
- [ ] Reviewed for credential exposure
- [ ] Validated input sanitization
- [ ] Checked for injection vulnerabilities
- [ ] Updated security documentation

## Documentation
- [ ] No documentation changes needed
- [ ] Updated README.md
- [ ] Updated CONTRIBUTING.md
- [ ] Updated workflow comments/descriptions
- [ ] Added inline code comments

## Deployment Notes
- [ ] Safe to deploy immediately
- [ ] Requires configuration changes before deployment
- [ ] Requires database/sheet setup before deployment
- [ ] Requires N8N restart after deployment

### Deployment Checklist
```
# Steps needed after merging (if any)
1. Update N8N workflow import
2. Configure new environment variables
3. Update Google Sheets permissions
4. Test webhook endpoints
```

## Reviewer Notes
Any specific areas you'd like reviewers to focus on or questions you have.

## Related Issues
Fixes # (issue number)
Related to # (issue number)

---

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own changes
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have tested the workflow with realistic data
- [ ] All CI checks pass