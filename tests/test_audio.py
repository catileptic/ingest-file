# -*- coding: utf-8 -*-
import datetime
from .support import TestCase


class AudioIngestorTest(TestCase):
    def test_audio(self):
        fixture_path, entity = self.fixture("memo.m4a")
        self.manager.ingest(fixture_path, entity)
        self.assertEqual(entity.first("processingStatus"), self.manager.STATUS_SUCCESS)
        self.assertEqual(entity.first("title"), "Core Media Audio")
        self.assertEqual(entity.first("generator"), "com.apple.VoiceMemos (iOS 11.4)")
        # with the change to Python 3.9 and the debian base image we are seeing a change
        # in the amount of data we are parsing here
        assert entity.get("authoredAt") == [
            datetime.datetime(2018, 6, 20, 12, 9, 28).isoformat(),
            datetime.datetime(2018, 6, 20, 12, 9, 42).isoformat(),
        ]
        self.assertEqual(entity.first("duration"), "2808")
        self.assertEqual(entity.first("samplingRate"), "44100")
        self.assertEqual(entity.schema.name, "Audio")
