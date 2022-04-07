from pathlib import Path
import shutil

from invoke import Collection, task

ns = Collection()
ns.configure({"package": "linux-gpib"})
ns.configure({"version": "4.3.2"})
ns.configure({"dir": {"source": "build/source"}})
ns.configure({"dir": {"build": "build/build"}})
ns.configure({"dir": {"package": "build/package"}})
ns.configure({"test_channel": "user/testing"})


def project_path():
    return Path(__file__).parents[0]


@task
def test(ctx):
    """Run conan package test (singular)"""

    pkg = ctx["package"]
    ver = ctx["version"]
    channel = ctx["test_channel"]

    with ctx.cd(str(project_path())):
        # ctx.run("conan create . user/testing")
        ctx.run(
            "conan test test_package {p}/{v}@{ch}".format(
                p=pkg, v=ver, pr=project_path(), ch=channel
            )
        )


@task
def source(ctx):
    """Run conan source routine"""

    src = ctx["dir"]["source"]
    with ctx.cd(str(project_path())):
        ctx.run(
            "conan source {pr} --source-folder={s}".format(
                s=project_path().joinpath(src), pr=project_path()
            )
        )


@task
def install(ctx):
    """Run conan install routine"""

    build = ctx["dir"]["build"]
    with ctx.cd(str(project_path())):
        ctx.run(
            "conan install {pr} --install-folder={b}".format(
                b=project_path().joinpath(build), pr=project_path()
            )
        )


@task
def build(ctx):
    """Run conan build routine"""

    src = ctx["dir"]["source"]
    build = ctx["dir"]["build"]
    with ctx.cd(str(project_path().joinpath(build))):
        ctx.run(
            "conan build {pr} --source-folder={s} --build-folder={b}".format(
                s=project_path().joinpath(src),
                b=project_path().joinpath(build),
                pr=project_path(),
            )
        )


@task
def package(ctx):
    """Run conan package routine"""

    src = ctx["dir"]["source"]
    build = ctx["dir"]["build"]
    package = ctx["dir"]["package"]

    with ctx.cd(str(project_path())):
        ctx.run(
            "conan package {pr} --source-folder={s} --build-folder={b} --package-folder={p}".format(
                s=project_path().joinpath(src),
                b=project_path().joinpath(build),
                p=package,
                pr=project_path(),
            )
        )


@task
def export(ctx):
    """Generate conan package in local cache"""

    src = ctx["dir"]["source"]
    build = ctx["dir"]["build"]
    channel = ctx["test_channel"]

    with ctx.cd(str(project_path())):
        ctx.run(
            "conan export-pkg {pr} {c} --source-folder={s} --build-folder={b}".format(
                s=project_path().joinpath(src),
                b=project_path().joinpath(build),
                c=channel,
                pr=project_path(),
            )
        )


@task(default=True)
def create(ctx, keep_source=False, keep_build=False):
    """Run the full conan package (test) flow"""

    channel = ctx["test_channel"]

    args = str()

    if keep_source:
        args += "--keep-source "

    if keep_build:
        args += "--keep-build "

    with ctx.cd(str(project_path())):
        ctx.run("conan create {pr} {c}".format(c=channel, pr=project_path()))


@task
def cleanup(ctx):
    """Remove temporary build, source, package directories"""

    src = ctx["dir"]["source"]
    build = ctx["dir"]["build"]
    package = ctx["dir"]["package"]
    pkg = ctx["package"]
    ver = ctx["version"]
    channel = ctx["test_channel"]

    try:
        shutil.rmtree(str(project_path().joinpath(src)))
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(str(project_path().joinpath(build)))
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(str(project_path().joinpath(package)))
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(str(project_path().joinpath("test_package").joinpath("build")))
    except FileNotFoundError:
        pass

    ctx.run(
        "conan search {p}/{v}@{c} 2>/dev/null && conan remove {p}/{v}@{c}".format(
            p=pkg, v=ver, c=channel
        ),
        warn=True,
    )


ns.add_task(test)
ns.add_task(source)
ns.add_task(install)
ns.add_task(build)
ns.add_task(package)
ns.add_task(export)
ns.add_task(create)
ns.add_task(cleanup)
