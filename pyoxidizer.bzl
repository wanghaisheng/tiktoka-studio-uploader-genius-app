# pyoxidizer.bzl

def make_dist():
    return default_python_distribution(python_version="3.10")


def make_policy(dist):
    policy = dist.make_python_packaging_policy()
    policy.extension_module_filter = "no-copyleft"
    policy.bytecode_optimize_level_two = True
    return policy


def make_config(dist):
    config = dist.make_python_interpreter_config()
    config.run_module = "main"
    return config


def make_exe(dist, policy, config):
    exe = dist.to_python_executable(
        name="uploadergenius",
        packaging_policy=policy,
        config=config,
    )
    exe.windows_runtime_dlls_mode = "always"
    exe.windows_subsystem = "console"

    # Include requirements and the root module.
    exe.add_python_resources(
        exe.pip_install(["-r", "requirements.txt"])
    )
    exe.add_python_resources(
        exe.read_package_root(path=".", packages=["main"])
    )

    return exe


def make_embedded_resources(exe):
    return exe.to_embedded_resources()


def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)
    return files


# Dynamically enable automatic code signing.
def register_code_signers():
    if not VARS.get("ENABLE_CODE_SIGNING"):
        return


# Call our function to set up automatic code signers.
register_code_signers()


register_target("dist", make_dist)
register_target("policy", make_policy, depends=["dist"], default=True)
register_target("config", make_config, depends=["dist"], default=True)
register_target("exe", make_exe, depends=["dist", "policy", "config"], default=True)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)
resolve_targets()