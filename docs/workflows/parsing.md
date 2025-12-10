# Parse and Upload Action

**File:** `.github/actions/parse-and-upload/action.yml`

This custom composite action handles parsing benchmark logs and uploading
results to Elasticsearch/Kibana for visualization and analysis.

## Purpose

After each benchmark job completes, this action:

1. Parses the log file to extract timing and performance metrics
2. Combines parsed data with static configuration
3. Sends the data to LogStash for routing and storage in Elasticsearch/Kibana

## Architecture

The parse-and-upload action uses **LogStash as a routing service** to direct
benchmark data to the appropriate Kibana instance:

```
GitHub Actions → LogStash → Elasticsearch/Kibana
                (routing)
```

**Key architectural details:**

- **LogStash endpoint:** LogStash routes requests to the appropriate Kibana
  instance based on the `token` + `kind` combination
- **Authentication/Routing:** The `token` and `kind` fields are sent as part of
  the JSON document body (NOT as Bearer authentication in HTTP headers)
- **No traditional credentials:** This design eliminates the need for
  username/password authentication - routing is handled via the token+kind
  fields in the data payload

This routing approach allows different benchmark types and projects to be
automatically directed to their respective Kibana instances while maintaining a
single, simple integration point for GitHub Actions workflows.

## Inputs

| Input          | Description                      | Required | Example                                       |
| -------------- | -------------------------------- | -------- | --------------------------------------------- |
| `job-type`     | Type of job                      | Yes      | `rucio`, `evnt-native`                        |
| `log-file`     | Path to log file                 | Yes      | `rucio.log`                                   |
| `log-type`     | Type of log parser to use        | Yes      | `rucio`, `athena`, `coffea`, `ff`             |
| `cluster`      | Cluster name                     | Yes      | `UC-AF`, `SLAC-AF`, `BNL-AF`                  |
| `kibana-token` | Token for benchmark ID           | Yes      | From secrets                                  |
| `kibana-kind`  | Kind for benchmark ID            | Yes      | From secrets                                  |
| `kibana-uri`   | URI endpoint for sending data    | Yes      | From secrets                                  |
| `host`         | Hostname to identify the machine | Yes      | {% raw %} `${{ env.NODE_NAME }}` {% endraw %} |

## Implementation Steps

The action performs these steps:

### 1. Setup pixi

Sets up the `kibana` pixi environment with:

- Python 3.13
- elasticsearch package
- Other dependencies as needed

### 2. Parse and Upload

Runs the parsing script (provided by Juan):

```bash
pixi run -e kibana python parsing/scripts/ci_parse_and_send.py \
  --job-type <job-type> \
  --log-file <log-file> \
  --log-type <log-type> \
  --cluster <cluster> \
  --token <token> \
  --kind <kind> \
  --uri <kibana-uri> \
  --host <host>
```

## Data Structure

The parsed data sent to LogStash (which routes it to Kibana) follows this
structure:

```json
{
  "cluster": "UC-AF",
  "testType": "Rucio Download",
  "submitTime": 1234567890000,
  "queueTime": 0,
  "runTime": 3600,
  "payloadSize": 1073741824,
  "status": 0,
  "host": "HOSTNAME",
  "token": "<TOKEN>",
  "kind": "benchmark"
}
```

### Field Descriptions

| Field         | Type    | Description                                   | Source                                                                 |
| ------------- | ------- | --------------------------------------------- | ---------------------------------------------------------------------- |
| `cluster`     | String  | AF cluster name                               | Passed from workflow                                                   |
| `testType`    | String  | Job type description                          | Parsed from log/mapped                                                 |
| `submitTime`  | Integer | UTC timestamp (ms)                            | Parsed from log                                                        |
| `queueTime`   | Integer | Queue time (seconds)                          | Parsed from log                                                        |
| `runTime`     | Integer | Execution time (seconds)                      | Parsed from log                                                        |
| `payloadSize` | Integer | Output size (bytes)                           | Parsed from log                                                        |
| `status`      | Integer | Exit code (0=success)                         | Parsed from log                                                        |
| `host`        | String  | Hostname where job executed                   | Passed from workflow via {% raw %} `${{ env.NODE_NAME }}` {% endraw %} |
| `token`       | String  | Benchmark identifier AND LogStash routing key | Passed from workflow (secrets)                                         |
| `kind`        | String  | Benchmark type AND LogStash routing kind      | Passed from workflow (secrets)                                         |

### Static vs Parsed Fields

**Static fields** (from workflow configuration):

- `cluster` - Set per site (UC-AF, SLAC-AF, etc.)
- `token` - Benchmark identifier token AND LogStash routing key
- `kind` - Benchmark kind/category AND LogStash routing kind
- `host` - Hostname from workflow environment ({% raw %} `${{ env.NODE_NAME }}`
  {% endraw %})

**Parsed fields** (extracted from logs):

- `testType` - Determined from job type or log content
- `submitTime` - Start timestamp from log
- `queueTime` - Time waiting before execution
- `runTime` - Total execution duration
- `payloadSize` - Size of output files
- `status` - Job exit code

**Note:** The `token` and `kind` fields are included in the JSON document body
sent to LogStash, where they serve the dual purpose of identifying the benchmark
and routing the data to the appropriate Kibana instance.

## Failure Handling

The action uses `continue-on-error: true` in workflows, which means:

- **Parsing failures don't fail the benchmark job**
- Logs are always uploaded as artifacts
- Parsing errors are visible in workflow logs
- Benchmarks complete successfully even if Kibana upload fails

This design ensures benchmark execution is never blocked by parsing/upload
issues.

## Usage Example

{% raw %}

```yaml
- name: parse and upload to kibana
  if: always() # Run even if benchmark failed
  uses: ./.github/actions/parse-and-upload
  with:
    job-type: ${{ github.job }}
    log-file: rucio.log
    log-type: rucio
    cluster: UC-AF
    kibana-token: ${{ secrets.KIBANA_TOKEN }}
    kibana-kind: ${{ secrets.KIBANA_KIND }}
    kibana-uri: ${{ secrests.KIBANA_URI }}
    host: ${{ env.NODE_NAME }}
  continue-on-error: true # Don't fail job if parsing fails
```

{% endraw %}

## LogStash/Elasticsearch Configuration

Data is sent to LogStash, which routes it to Elasticsearch:

- **LogStash endpoint:** this acts as routing service
- **Elasticsearch index:** `af_benchmarks`
- **Protocol:** HTTPS
- **Routing/Authentication:** Via `token` + `kind` fields in the JSON document
  body

The `token` and `kind` fields serve a dual purpose:

1. **Benchmark identification:** Uniquely identify and categorize the benchmark
   run
2. **LogStash routing:** Direct the data to the appropriate Kibana instance

This body-based routing mechanism eliminates the need for traditional HTTP
authentication headers or stored credentials.

## Debugging

### Viewing Parsing Logs

1. Go to the workflow run in GitHub Actions
2. Click on the specific job
3. Expand the "parse and upload to kibana" step
4. Review the output for parsing errors

### Common Parsing Issues

**Log file not found:**

- Verify the log file path matches the actual output
- Check that the benchmark script completed
- Look for the file in workflow artifacts

**Parsing errors:**

- Check log file format matches expected structure
- Verify parsing script handles this job type
- Review error messages in workflow logs

**Upload failures:**

- Check network connectivity to LogStash endpoint
- Verify `token` and `kind` values are correctly set
- Ensure the `af_benchmarks` index exists in Elasticsearch

### Testing Locally

Test parsing without uploading:

```bash
pixi shell -e kibana

python parsing/scripts/ci_parse_and_send.py \
  --job-type rucio \
  --log-file path/to/rucio.log \
  --log-type rucio \
  --cluster UC-AF \
  --token TOKEN \
  --kind benchmark \
  --uri KIBANA_URI \
  --host HOSTNAME \
  --dry-run  # If supported by parsing script
```

## Integration with Other Workflows

This action is currently used by:

- [UChicago Benchmark Workflow](benchmarks.md) - All 10 benchmark jobs

Can be extended to:

- SLAC benchmark workflows
- BNL benchmark workflows
- NERSC benchmark workflows

## Next Steps

- Review the [UChicago benchmark workflow](benchmarks.md)
- Learn about [local development](development.md)
- Understand the [pixi environments](index.md#pixi-environments)
