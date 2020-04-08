
# Implementing Jaeger Tracing

### Adding Service name in `jaegerTracing.py`
***
```python
service_name = "ShortlistCadidatesForJobAPI"
```

## Importing Libraries

### Flask API Tracing
#### Automated Traces All Routes
```python
# Distributed Tracing
import jaegerTracing
tracer = jaegerTracing.getTracerInstance()
from flask_opentracing import FlaskTracing
tracing = FlaskTracing(tracer, True, app)
```
#### Manual Traces All Routes
##### Regex Pattern
```python
@app.route
```
##### Regex Replace
```python
@tracing.trace()
$0
```

### Batch Editing in Client files
#### Import Libraries without Regex
```python
# Distributed Tracing
from opentracing_instrumentation.request_context import get_current_span, span_in_context
import jaegerTracing
tracer = jaegerTracing.getTracerInstance()
from opentracing.propagation import Format
```
#### Import Libraries via Regrx
##### Regex Pattern
```python
class\s\w*\(\):
```
##### Regex Replace
```python
# Distributed Tracing
from opentracing_instrumentation.request_context import get_current_span, span_in_context
import jaegerTracing
tracer = jaegerTracing.getTracerInstance()
from opentracing.propagation import Format
 
$0
```
## Injecting Spans
### Methods with try-except

!!! tip
    You can also have to check whether there exist any method without having class. Mehthod with class may have no leading spaces in it which we are using in the regex.


`(def\s([\w]+)\s?\(self,*\s*([\w,\s=']*)\)\s*:)\s*
    (try:)`


##### Regex Pattern
```
(    )(def\s([\w]+)\s?\(self,*\s*([\w,\s=']*)\)\s*:)\s*
        (try:)
```
##### Regex Replace
```
$2
    $5
        with tracer.start_active_span('$3') as scope:
            scope.span.set_tag('args', [$4])
```
### Methods without try-except
##### Regex Pattern
```
(    )(def\s([\w]+)\s?\(self,*\s*([\w,\s=']*)\)\s*:)
```
##### Regex Replace
```
$2
    with tracer.start_active_span('$3') as scope:
        scope.span.set_tag('args', [$4])
```

!!! Caution
    Indentation of the file reduces the starting spaces upto 4 spaces with cause `except` to deviate from consective `try`. You should have to replace the spaces accouding to the starting try block.

### Handling Exception
##### Regex Pattern
```
(\s*)except Exception as ex:
```
##### Regex Replace
```
$0
    $1scope.span.set_tag('Exception', ex)
```

### Handling Return Statuses

!!! Tip
    Make sure `regex` button is pressed in vscode search field.

#### 01 - Return `Variable Names`
##### Regex Pattern
```
(\s*)return jsonify\(([\w]*)\)
```

##### Regex Replace
```
$1scope.span.set_tag('response', $2)$0
```

#### 02 - Return `String`
##### Regex Pattern
```
(\s*)return jsonify\("([\w\s]*)"\)
```
##### Regex Replace
```
$1scope.span.set_tag('response', '$2')$0
```
#### 03 - Return `Json Data`
##### Regex Pattern 
```
(\s*)return jsonify\(\{(['\w:,\s\[\].+"\(\)]*)\}\)
```
##### Regex Replace
```
$1scope.span.set_tag('response', dict({$2}))$0
```
#### 04 - Return `Graph Database Collections Query`
##### Regex Pattern 
```
(\s*)return list\(self\.Collection\.find\((\w*)
```
##### Regex Replace
```
$1scope.span.set_tag('response', $2)$0
```
#### 05 - Return `response.json()`
##### Regex Pattern
```
(\s*)return response\.json\(\)
```
##### Regex Replace
```
$1scope.span.set_tag('response', response.json())
$0
```


!!! Tip
    After applying regex, methods were reindented from their actual location, you have to manually indent the methods. ++ctrl+close-bracket++

## Keywords Used in All APIS

`args`
`response`

## Branches Created for Tracing
### Names of Branches
```
git branch
```

- **Tracing_skill_social**
    - Skill_Social/endorse_skill_api
    - Skill_Social/rate_skill_api
    - Skill_Social/skill_comment_api

- **Tracing_jobAPIs(all)**
    - job_application_state_change_notice
    - job_application_state_change_save
    - job_application_state_change_web_notification
    - job_application_state_email_log_to_mdb
    - job_application_state_management_api
    - job_comments_api
- **Tracing-bkmrk-candid,-candid-job-app-mgmt-api,-bkmrk-job-api**
    - bookmark_candidates_api
    - candidate_job_application_management_api
    - bookmark_job_api
- **Tracing-JobPost-API**
    - revamp_laravel_to_python_apis
        - jobpost_python_apis
- **jeager_implementation_organizationalDataAPI**
    - organizational_data
- **shortlistedCandidate_tracing_with_Jaeger**
    - revamp_laravel_to_python_apis
        - admin_operation_python_apis          
        - Consumer_UserName_Image_Storage
        - profile_python_apis
        - registeration_python_service_apis



regex

(http://[\w./-:'+\s-]*)




























