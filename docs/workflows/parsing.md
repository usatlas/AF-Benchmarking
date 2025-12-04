# Parse and Upload Action

**File:** `.github/actions/parse-and-upload/action.yml`

This custom composite action handles parsing benchmark logs and uploading results to Elasticsearch/Kibana for visualization and analysis.

## Purpose

After each benchmark job completes, this action:

1. Parses the log file to extract timing and performance metrics
2. Combines parsed data with static configuration
3. Sends the data to Elasticsearch/Kibana for storage and visualization

## Inputs

| Input | Description | Required | Example |
|-------|-------------|----------|---------|
| `job-type` | Type of job | Yes | `rucio`, `evnt-native` |
| `log-file` | Path to log file | Yes | `rucio.log` |
| `cluster` | Cluster name | Yes | `UC-AF`, `SLAC-AF`, `BNL-AF` |
| `es-username` | Elasticsearch username | Yes | From secrets |
| `es-password` | Elasticsearch password | Yes | From secrets |
| `kibana-token` | Token for benchmark ID | Yes | From secrets |
| `kibana-kind` | Kind for benchmark ID | Yes | From secrets |

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
  --cluster <cluster> \
  --es-username <username> \
  --es-password <password> \
  --token <token> \
  --kind <kind>
```

## Data Structure

The parsed data sent to Kibana follows this structure:

```json
{
  "cluster": "UC-AF",
  "testType": "Rucio Download",
  "submitTime": 1234567890000,
  "queueTime": 0,
  "runTime": 3600,
  "payloadSize": 1073741824,
  "status": 0,
  "host": "login01.af.uchicago.edu",
  "token": "bench23f2f2ef",
  "kind": "benchmark"
}
```

### Field Descriptions

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `cluster` | String | AF cluster name | Passed from workflow |
| `testType` | String | Job type description | Parsed from log/mapped |
| `submitTime` | Integer | UTC timestamp (ms) | Parsed from log |
| `queueTime` | Integer | Queue time (seconds) | Parsed from log |
| `runTime` | Integer | Execution time (seconds) | Parsed from log |
| `payloadSize` | Integer | Output size (bytes) | Parsed from log |
| `status` | Integer | Exit code (0=success) | Parsed from log |
| `host` | String | Execution host | Parsed from log |
| `token` | String | Benchmark identifier | Passed from workflow |
| `kind` | String | Benchmark type | Passed from workflow |

### Static vs Parsed Fields

**Static fields** (from workflow configuration):

- `cluster` - Set per site (UC-AF, SLAC-AF, etc.)
- `token` - Benchmark identifier token
- `kind` - Benchmark kind/category

**Parsed fields** (extracted from logs):

- `testType` - Determined from job type or log content
- `submitTime` - Start timestamp from log
- `queueTime` - Time waiting before execution
- `runTime` - Total execution duration
- `payloadSize` - Size of output files
- `status` - Job exit code
- `host` - Hostname where job ran

## Failure Handling

The action uses `continue-on-error: true` in workflows, which means:

- **Parsing failures don't fail the benchmark job**
- Logs are always uploaded as artifacts
- Parsing errors are visible in workflow logs
- Benchmarks complete successfully even if Kibana upload fails

This design ensures benchmark execution is never blocked by parsing/upload issues.

## Usage Example

{% raw %}
```yaml
- name: parse and upload to kibana
  if: always()  # Run even if benchmark failed
  uses: ./.github/actions/parse-and-upload
  with:
    job-type: ${{ github.job }}
    log-file: rucio.log
    cluster: UC-AF
    es-username: ${{ secrets.ES_USERNAME }}
    es-password: ${{ secrets.ES_PASSWORD }}
    kibana-token: ${{ secrets.KIBANA_TOKEN }}
    kibana-kind: ${{ secrets.KIBANA_KIND }}
  continue-on-error: true  # Don't fail job if parsing fails
```
{% endraw %}

## Elasticsearch Configuration

Data is sent to:

- **Host:** `atlas-kibana.mwt2.org:9200`
- **Index:** `af_benchmarks`
- **Protocol:** HTTPS
- **Authentication:** Basic auth (username/password)

Credentials are stored as GitHub repository secrets.

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

- Verify Elasticsearch credentials are valid
- Check network connectivity to Kibana
- Ensure the `af_benchmarks` index exists

### Testing Locally

Test parsing without uploading:

```bash
pixi shell -e kibana

python parsing/scripts/ci_parse_and_send.py \
  --job-type rucio \
  --log-file path/to/rucio.log \
  --cluster UC-AF \
  --es-username test \
  --es-password test \
  --token bench23f2f2ef \
  --kind benchmark \
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
