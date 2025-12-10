# UChicago Benchmark Workflow

**File:** `.github/workflows/uchicago.yml`

This workflow runs automated benchmark jobs at the UChicago Analysis Facility to
measure performance across different job types and configurations.

## Trigger

The workflow runs:

- **Every 6 hours** (on schedule: `0 */6 * * *`)
- **On pull requests** to `main`
- **Manually** via `workflow_dispatch`

## Benchmark Jobs

The workflow runs 10 parallel benchmark jobs on `arc-runner-set-uchicago`
runners:

| Job                   | Script                                                           | Log File                 | Description                           |
| --------------------- | ---------------------------------------------------------------- | ------------------------ | ------------------------------------- |
| `rucio`               | `./Rucio/rucio_script.sh`                                        | `rucio.log`              | Download data using Rucio             |
| `evnt-native`         | `./EVNT/UC/Native/run_evnt_native_batch.sh`                      | `log.generate`           | EVNT generation (native)              |
| `evnt-el9`            | `./EVNT/UC/EL9/run_evnt_el9_batch.sh`                            | `log.generate`           | EVNT generation (EL9 container)       |
| `evnt-centos7`        | `./EVNT/UC/CentOS7/run_evnt_centos7_batch.sh`                    | `log.generate`           | EVNT generation (CentOS7 container)   |
| `truth3-native`       | `./TRUTH3/UC/Native/run_truth3_native_batch.sh`                  | `log.Derivation`         | TRUTH3 derivation (native)            |
| `truth3-el9`          | `./TRUTH3/UC/EL9/run_truth3_el9_batch.sh`                        | `log.Derivation`         | TRUTH3 derivation (EL9 container)     |
| `truth3-centos7`      | `./TRUTH3/UC/CentOS7/run_truth3_centos7_batch.sh`                | `log.EVNTtoDAOD`         | TRUTH3 derivation (CentOS7 container) |
| `coffea`              | `./NTuple_Hist/coffea/UC/run_example.sh`                         | `coffea_hist.log`        | NTuple to histogram (Coffea)          |
| `event-loop-columnar` | `./NTuple_Hist/event_loop/UC/columnar/run_eventloop_arrays.sh`   | `eventloop_arrays.log`   | Event loop (columnar)                 |
| `event-loop-standard` | `./NTuple_Hist/event_loop/UC/standard/run_eventloop_noarrays.sh` | `eventloop_noarrays.log` | Event loop (standard)                 |
| `FF`                  | `./NTuple_Hist/fastframes/UC/run_ff.sh`                          | `ff.log`                 | NTuple to histogram (FastFrames)      |

## Workflow Steps

Each job follows this pattern:

1. **Checkout** - Clone the repository
2. **Setup Globus** (if required) - Configure VOMS certificates for data access
3. **Execute** - Run the benchmark script
4. **Parse and Upload** - Parse logs and send results to Kibana (via
   [custom action](parsing.md))
5. **Upload Logs** - Store log files as GitHub artifacts

### Example Job Structure

{% raw %}

```yaml
rucio:
  runs-on: arc-runner-set-uchicago
  steps:
    - uses: actions/checkout@v5

    - uses: ./.github/actions/setup-globus
      with:
        voms-usercert: ${{ secrets.VOMS_USERCERT }}
        voms-userkey: ${{ secrets.VOMS_USERKEY }}

    - name: execute
      run: ./Rucio/rucio_script.sh uchicago
      shell: bash
      env:
        VOMS_PASSWORD: ${{ secrets.VOMS_PASSWORD }}

    - name: parse and upload to kibana
      if: always()
      uses: ./.github/actions/parse-and-upload
      with:
        job-type: ${{ github.job }}
        log-file: rucio.log
        cluster: UC-AF
        es-username: ${{ secrets.ES_USERNAME }}
        es-password: ${{ secrets.ES_PASSWORD }}
        kibana-token: ${{ secrets.KIBANA_TOKEN }}
        kibana-kind: ${{ secrets.KIBANA_KIND }}
      continue-on-error: true

    - name: upload log
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: ${{ github.job }}-logs
        path: rucio.log
```

{% endraw %}

## Monitoring Results

### Viewing Workflow Runs

1. Go to the repository's
   [Actions tab](https://github.com/usatlas/af-benchmarking/actions)
2. Select the "uchicago" workflow
3. Click on a specific run to see job details

### Checking Logs

- **Benchmark logs:** Download from workflow artifacts (available for 90 days)
- **Workflow logs:** View in the GitHub Actions UI
- **Parsing errors:** Check the "parse and upload to kibana" step logs

### Common Issues

**Benchmark job failures:**

- Check VOMS credentials are valid
- Verify runner has network access to required resources
- Review benchmark script logs in artifacts

**Parsing failures:**

- Check that log files are generated correctly
- Verify Elasticsearch credentials are valid
- Review parsing script output in workflow logs

## Benchmark Types Explained

### Rucio Download

Downloads ATLAS data files using the Rucio data management system. Measures data
transfer performance.

**Documentation:**
[Rucio Download Tutorial](https://atlassoftwaredocs.web.cern.ch/internal-links/grid-tutorial/rucio-download-files/)

### EVNT Generation

Generates Monte Carlo event files (EVNT format) using different runtime
environments.

**Documentation:**
[EVNT Production Tutorial](https://atlassoftwaredocs.web.cern.ch/analysis-software/AnalysisSWTutorial/mc_generation/)

### TRUTH3 Derivation

Creates TRUTH3 derivation files from EVNT files for truth-level analysis.

**Documentation:**
[TRUTH3 Derivation Tutorial](https://atlassoftwaredocs.web.cern.ch/analysis-software/AnalysisSWTutorial/mc_truth_derivation/)

### NTuple to Histogram

Converts NTuple ROOT files to histograms using various frameworks:

- **Coffea:** Python-based columnar analysis framework
- **FastFrames:** C++ framework for fast ROOT analysis
- **EventLoop:** Traditional ATLAS event processing framework

## Next Steps

- Learn about the [parsing and upload action](parsing.md)
- See the [development guide](development.md) for adding new benchmarks
- Check [documentation workflow](documentation.md) details
