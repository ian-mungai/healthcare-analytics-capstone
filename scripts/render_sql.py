"""Render a capstone SQL template with a validated local S3 bucket, without executing SQL."""

import argparse
import os
import re
import sys
from pathlib import Path


def render_sql(template: Path, bucket: str) -> str:
    """Replace the bucket token in a repository SQL template; reject unsafe configuration."""
    sql_root = Path(__file__).resolve().parents[1] / "sql"
    resolved = template.resolve()
    if not resolved.is_relative_to(sql_root) or resolved.suffix != ".sql":
        raise ValueError("Choose a .sql template under this project's sql directory")
    if (
        not re.fullmatch(r"[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]", bucket)
        or ".." in bucket
        or ".-" in bucket
        or "-." in bucket
        or re.fullmatch(r"\d+\.\d+\.\d+\.\d+", bucket)
        or bucket.startswith(("xn--", "sthree-", "amzn-s3-demo-"))
        or bucket.endswith(("-s3alias", "--ol-s3", ".mrap", "--x-s3", "--table-s3"))
    ):
        raise ValueError("Set S3_BUCKET to a valid bucket name, without a URL, path or template token")
    sql = resolved.read_text(encoding="utf-8")
    if "<S3_BUCKET>" not in sql:
        raise ValueError("The selected SQL file has no S3_BUCKET token")
    return sql.replace("<S3_BUCKET>", bucket)


def main() -> None:
    """Write rendered SQL to stdout; configuration errors contain no supplied values."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    args = parser.parse_args()
    try:
        sql = render_sql(args.template, os.environ.get("S3_BUCKET", "").strip())
    except (OSError, ValueError):
        parser.error("Use a readable repository SQL template and a valid S3_BUCKET environment variable")
    sys.stdout.write(sql)


if __name__ == "__main__":
    main()
