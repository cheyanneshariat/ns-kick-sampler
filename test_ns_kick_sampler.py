"""Run with python -m unittest."""

import unittest

import numpy as np

from ns_kick_sampler import sample_kick_speeds, sample_kick_vectors


class KickVectorTests(unittest.TestCase):
    def test_magnitudes_match_speed_sampler(self):
        speeds = sample_kick_speeds(10_000, seed=67)
        vectors = sample_kick_vectors(10_000, seed=67)
        self.assertEqual(vectors.shape, (10_000, 3))
        np.testing.assert_allclose(np.linalg.norm(vectors, axis=1), speeds)
        self.assertTrue(np.all((speeds > 0.05) & (speeds < 1000)))

    def test_seed_reproducibility(self):
        np.testing.assert_array_equal(
            sample_kick_vectors(100, seed=7), sample_kick_vectors(100, seed=7)
        )
        rng = np.random.default_rng(7)
        self.assertFalse(np.array_equal(
            sample_kick_vectors(100, seed=rng), sample_kick_vectors(100, seed=rng)
        ))

    def test_empty_and_single_draw(self):
        self.assertEqual(sample_kick_vectors(0, seed=7).shape, (0, 3))
        self.assertEqual(sample_kick_vectors(np.int64(1), seed=7).shape, (1, 3))

    def test_invalid_counts(self):
        for count in (True, np.bool_(False), 1.5, "1"):
            with self.subTest(count=count), self.assertRaises(TypeError):
                sample_kick_vectors(count)
        with self.assertRaises(ValueError):
            sample_kick_vectors(-1)

    def test_isotropic_directions(self):
        vectors = sample_kick_vectors(200_000, seed=42)
        speeds = np.linalg.norm(vectors, axis=1)
        directions = vectors / speeds[:, None]
        np.testing.assert_allclose(directions.mean(axis=0), 0, atol=0.006)
        np.testing.assert_allclose(
            directions.T @ directions / len(directions), np.eye(3) / 3, atol=0.006
        )
        for axis in range(3):
            counts, _ = np.histogram(directions[:, axis], bins=10, range=(-1, 1))
            np.testing.assert_allclose(counts / len(directions), 0.1, atol=0.003)
        for mask in (speeds < 50, speeds >= 50):
            np.testing.assert_allclose(directions[mask].mean(axis=0), 0, atol=0.02)


if __name__ == "__main__":
    unittest.main()
