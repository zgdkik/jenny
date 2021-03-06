properties([
    parameters([
        string(name: 'JENNY_DOCKER_UID', defaultValue: '1000:1000',
                description: 'Should correspond to the uid:gid of the user running docker.'),
        string(name: 'JENNY_DOCKER_GID', defaultValue: '999',
                description: 'Should be the group ID of the docker installation.')
    ])
])

JENNY_DOCKER_UID = params.JENNY_DOCKER_UID ?: '1000:1000'
JENNY_DOCKER_GID = params.JENNY_DOCKER_GID ?: '999'

stage('Build Test Container') {
    node {
        deleteDir()
        checkout scm

        docker.build('jenny_test_junit',
                     'features/junit-support')

        docker.build('jenny_test_container')
              .inside("-v /var/run/docker.sock:/var/run/docker.sock:rw -v /tmp:/tmp:rw -u $JENNY_DOCKER_UID --group-add $JENNY_DOCKER_GID") {
                    checkout scm
                    try {
                        sh """
                            bin/test_jenny.py
                        """
                    } finally {
                        sh "cat /tmp/jenny_*.log"
                    }
        }
    }
}

