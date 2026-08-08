from f1_regulations_rag.ingestion.chunkers import HierarchicalChunker


def test_split_on_top_level_articles() -> None:
    text = (
        "ARTICLE B1: ORGANISATION OF A COMPETITION\n"
        "some body text here\n"
        "ARTICLE B2: FORMAT OF A COMPETITION\n"
        "more body text\n"
    )
    chunks = HierarchicalChunker().chunk(text)
    assert [c.article_number for c in chunks] == ["B1", "B2"]
    assert "some body text" in chunks[0].text


def test_split_on_sub_clauses() -> None:
    text = (
        "ARTICLE B5: TOTAL TIME CLASSIFIED SESSIONS (TTCS)\n"
        "B5.13 Safety Car (SC)\n"
        "details about the safety car\n"
        "B5.14 Suspension Procedure(s)\n"
        "details about suspension\n"
    )
    chunks = HierarchicalChunker().chunk(text)
    assert [c.article_number for c in chunks] == ["B5", "B5.13", "B5.14"]


def test_table_row_labels_do_not_split() -> None:
    """Bare numbers like '1.1' are table labels in these PDFs, not articles."""
    text = "1.1 Brake friction material may be removed\n1.2 The brake system may be bled.\n"
    chunks = HierarchicalChunker().chunk(text)
    assert len(chunks) == 1
    assert chunks[0].article_number is None


def test_no_boundaries_yields_single_chunk() -> None:
    chunks = HierarchicalChunker().chunk("just some plain text")
    assert len(chunks) == 1
    assert chunks[0].article_number is None


def test_empty_text_yields_no_chunks() -> None:
    assert HierarchicalChunker().chunk("") == []
