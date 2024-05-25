#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import io
import json
import logging
import sys
import typing
import unittest
import warnings

import daiquiry


class TestDaiquiry(unittest.TestCase):
    def tearDown(self) -> None:
        # Be sure to reset the warning capture
        logging.captureWarnings(False)
        super(TestDaiquiry, self).tearDown()

    def test_setup(self) -> None:
        daiquiry.setup()
        daiquiry.setup(level=logging.DEBUG)
        daiquiry.setup(program_name="foobar")

    def test_setup_json_formatter(self) -> None:
        stream = io.StringIO()
        daiquiry.setup(
            outputs=(
                daiquiry.output.Stream(
                    stream, formatter=daiquiry.formatter.JSON_FORMATTER
                ),
            )
        )
        daiquiry.getLogger(__name__).warning("foobar")
        expected: dict[str, typing.Any] = {"message": "foobar"}
        if sys.version_info >= (3, 12):
            expected.update({"taskName": None})
        self.assertEqual(expected, json.loads(stream.getvalue()))

    def test_setup_json_formatter_with_extras(self) -> None:
        stream = io.StringIO()
        daiquiry.setup(
            outputs=(
                daiquiry.output.Stream(
                    stream, formatter=daiquiry.formatter.JSON_FORMATTER
                ),
            )
        )
        daiquiry.getLogger(__name__).warning("foobar", foo="bar")
        expected: dict[str, typing.Any] = {"message": "foobar", "foo": "bar"}
        if sys.version_info >= (3, 12):
            expected.update({"taskName": None})
        self.assertEqual(expected, json.loads(stream.getvalue()))

    def test_get_logger_set_level(self) -> None:
        logger = daiquiry.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    def test_capture_warnings(self) -> None:
        stream = io.StringIO()
        daiquiry.setup(outputs=(daiquiry.output.Stream(stream),))
        warnings.warn("omg!")
        line = stream.getvalue()
        self.assertIn("WARNING  py.warnings: ", line)
        self.assertIn(
            "daiquiry/tests/test_daiquiry.py:71: "
            'UserWarning: omg!\n  warnings.warn("omg!")\n',
            line,
        )

    def test_no_capture_warnings(self) -> None:
        stream = io.StringIO()
        daiquiry.setup(
            outputs=(daiquiry.output.Stream(stream),), capture_warnings=False
        )
        warnings.warn("omg!")
        self.assertEqual("", stream.getvalue())

    def test_set_default_log_levels(self) -> None:
        daiquiry.set_default_log_levels((("amqp", "debug"), ("urllib3", "warn")))

    def test_parse_and_set_default_log_levels(self) -> None:
        daiquiry.parse_and_set_default_log_levels(("urllib3=warn", "foobar=debug"))

    def test_string_as_setup_outputs_arg(self) -> None:
        daiquiry.setup(outputs=("stderr", "stdout"))

        if daiquiry.handlers.syslog is not None:  # type: ignore[attr-defined]
            daiquiry.setup(outputs=("syslog",))

        if daiquiry.handlers.journal is not None:  # type: ignore[attr-defined]
            daiquiry.setup(outputs=("journal",))

    def test_special_kwargs(self) -> None:
        daiquiry.getLogger(__name__).info(
            "foobar", foo="bar", exc_info=True, stack_info=True
        )


def test_extra_with_two_loggers() -> None:
    stream = io.StringIO()
    daiquiry.setup(outputs=(daiquiry.output.Stream(stream),))
    log1 = daiquiry.getLogger("foobar")
    log1.error("argh")
    log2 = daiquiry.getLogger("foobar", key="value")
    log2.warning("boo")
    lines = stream.getvalue().strip().split("\n")
    assert lines[0].endswith("ERROR    foobar: argh")
    assert lines[1].endswith("WARNING  foobar [key: value]: boo")
