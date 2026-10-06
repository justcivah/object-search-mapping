FROM osrf/ros:humble-desktop
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=1000

# repository OSRF and ignition fortress
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        lsb-release \
        gnupg \
    && curl -fsSL https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends ignition-fortress \
    && rm -rf /var/lib/apt/lists/*

# ros2 and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-colcon-common-extensions \
        python3-vcstool \
        libgl1-mesa-dri mesa-vulkan-drivers \
        mesa-utils \
        sudo \
        nano \
        git \
    && rm -rf /var/lib/apt/lists/*

# clearpath and ros-gazebo bridge
RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-humble-ros-gz \
        ros-humble-clearpath-simulator \
    && rm -rf /var/lib/apt/lists/*

# create the user with the host uid/gid
RUN set -eux; \
    # if a group with that GID does not exist create it
    if ! getent group "$USER_GID" > /dev/null; then \
        groupadd --gid "$USER_GID" "$USERNAME"; \
    fi; \
    # check if a user already had that UID
    # if it exist, existing_user will contain that username, otherwise an empty string
    existing_user="$(getent passwd "$USER_UID" | cut -d: -f1 || true)"; \
    # if existing_user it not empty, rename the current user to USERNAME
    if [ -n "$existing_user" ]; then \
        usermod --login "$USERNAME" --home "/home/$USERNAME" --move-home \
            --gid "$USER_GID" --shell /bin/bash "$existing_user"; \
    # otherwise if existing_user is empty, just create a new user
    else \
        useradd --uid "$USER_UID" --gid "$USER_GID" -m -s /bin/bash "$USERNAME"; \
    fi; \
    usermod -aG video "$USERNAME"; \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > "/etc/sudoers.d/$USERNAME"

USER $USERNAME
WORKDIR /home/$USERNAME/ros2_ws
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
    && echo "[ -f ~/ros2_ws/install/setup.bash ] && source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
