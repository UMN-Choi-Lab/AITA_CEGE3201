"""
Document ingestion for AITA 3201.
Custom collectors for non-standard directory layout (Slides (1)/, Homework handouts (1)/).
"""

import os

from aita_core.ingest import (
    get_week_for_filename, load_pdf, load_tex,
    collect_syllabus, collect_wikibook, run_ingestion,
)
from config import CONFIG


def _week_for(filename):
    return get_week_for_filename(
        filename, CONFIG.topic_num_to_week, CONFIG.hw_num_to_week,
        CONFIG.lab_num_to_week, CONFIG.study_guide_to_week,
    )


def _slides_dir():
    d = os.path.join(CONFIG.course_materials_dir, "Slides (1)", "Slides")
    if not os.path.isdir(d):
        d = os.path.join(CONFIG.course_materials_dir, "Slides", "Slides")
    return d


def collect_handouts(config):
    """Collect handout PDFs from Handouts/ directory (flat layout with study guides).

    Prefers .tex over .pdf for study guides when both exist (better math/table quality).
    """
    docs = []
    handouts_dir = os.path.join(CONFIG.course_materials_dir, "Handouts")
    if not os.path.isdir(handouts_dir):
        # Fall back to extracting Handout.pdf from inside each slide topic directory
        slides_dir = _slides_dir()
        if not os.path.isdir(slides_dir):
            print("  Warning: no handouts directory found")
            return docs
        for topic_name in sorted(os.listdir(slides_dir)):
            topic_path = os.path.join(slides_dir, topic_name)
            if not os.path.isdir(topic_path):
                continue
            handout_pdf = os.path.join(topic_path, "Handout.pdf")
            if os.path.exists(handout_pdf):
                label = f"Handout: {topic_name}"
                week = _week_for(topic_name)
                print(f"  Loading {label} (week {week})")
                docs.extend(load_pdf(handout_pdf, label, max_week=week))
        return docs

    # Map .tex study guide files to their canonical label so we can skip the PDF version
    _TEX_STUDY_GUIDES = {
        "midterm1.tex": "Midterm 1 study guide",
        "midterm2.tex": "Midterm 2 study guide",
        "final.tex": "Final exam study guide",
        "formulasheet.tex": "Final exam formula sheet",
    }
    loaded_labels = set()

    # Load .tex study guides first (better math/table quality than PDF)
    for tex_file, label in sorted(_TEX_STUDY_GUIDES.items()):
        tex_path = os.path.join(handouts_dir, tex_file)
        if os.path.exists(tex_path):
            full_label = f"Handout: {label}"
            week = _week_for(label)
            print(f"  Loading {full_label} (LaTeX, week {week})")
            docs.extend(load_tex(tex_path, full_label, max_week=week))
            loaded_labels.add(label)

    # Load PDFs, skipping those already loaded from .tex
    for filename in sorted(os.listdir(handouts_dir)):
        if not filename.endswith(".pdf"):
            continue
        if "syllabus" in filename.lower():
            continue  # collected separately by collect_syllabus
        name = filename.removesuffix(".pdf")
        if name in loaded_labels:
            print(f"  Skipping {filename} (using .tex version)")
            continue
        file_path = os.path.join(handouts_dir, filename)
        label = f"Handout: {name}"
        week = _week_for(name)
        print(f"  Loading {label} (week {week})")
        docs.extend(load_pdf(file_path, label, max_week=week))
    return docs


def collect_homework(config):
    docs = []
    hw_dir = os.path.join(CONFIG.course_materials_dir, "Homework handouts (1)", "Homework handouts")
    if not os.path.isdir(hw_dir):
        hw_dir = os.path.join(CONFIG.course_materials_dir, "Homework handouts", "Homework handouts")
    if not os.path.isdir(hw_dir):
        print("  Warning: homework handouts directory not found")
        return docs
    for filename in sorted(os.listdir(hw_dir)):
        if not filename.endswith(".pdf"):
            continue
        if "solution" in filename.lower():
            print(f"  Skipping (solution): {filename}")
            continue
        file_path = os.path.join(hw_dir, filename)
        label = f"Homework: {filename}"
        week = _week_for(filename)
        print(f"  Loading {label} (week {week})")
        docs.extend(load_pdf(file_path, label, max_week=week))
    return docs


def collect_slides(config):
    docs = []
    slides_dir = _slides_dir()
    if not os.path.isdir(slides_dir):
        print("  Warning: slides directory not found")
        return docs
    for topic_name in sorted(os.listdir(slides_dir)):
        topic_path = os.path.join(slides_dir, topic_name)
        if not os.path.isdir(topic_path):
            continue
        label = f"Slides: {topic_name}"
        week = _week_for(topic_name)
        content_tex = os.path.join(topic_path, "content.tex")
        if os.path.exists(content_tex):
            print(f"  Loading {label} (LaTeX, week {week})")
            docs.extend(load_tex(content_tex, label, max_week=week))
        else:
            notes_pdf = os.path.join(topic_path, "Notes.pdf")
            if os.path.exists(notes_pdf):
                print(f"  Loading {label} (PDF, week {week})")
                docs.extend(load_pdf(notes_pdf, label, max_week=week))
    return docs


def collect_practice_exams(config):
    """Load practice exam PDFs from Homeworks/Homeworks/Practice/."""
    docs = []
    practice_dir = os.path.join(CONFIG.course_materials_dir, "Homeworks", "Homeworks", "Practice")
    if not os.path.isdir(practice_dir):
        print("  No practice exam directory found")
        return docs
    for filename in sorted(os.listdir(practice_dir)):
        if not filename.endswith(".pdf"):
            continue
        if "solution" in filename.lower():
            print(f"  Skipping (solution): {filename}")
            continue
        file_path = os.path.join(practice_dir, filename)
        label = f"Practice Exam: {filename}"
        # Practice exams are available from week 1 (general review material)
        week = 1
        print(f"  Loading {label} (week {week})")
        docs.extend(load_pdf(file_path, label, max_week=week))
    return docs


if __name__ == "__main__":
    run_ingestion(CONFIG, collectors=[
        ("lecture handouts", collect_handouts),
        ("homework questions", collect_homework),
        ("practice exams", collect_practice_exams),
        ("slide content", collect_slides),
        ("syllabus", collect_syllabus),
        ("textbook (wikibook)", collect_wikibook),
    ])
