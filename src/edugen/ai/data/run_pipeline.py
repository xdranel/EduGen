from edugen.ai.data.pipeline import DataPipeline


def main() -> None:
    result = DataPipeline().run()
    print(f"Processed {result.statistics.total_samples} samples")


if __name__ == "__main__":
    main()
