import pytest


@pytest.mark.django_db(transaction=True)
def test_style_parameters(authenticated_api_client, image_file_geotiff):
    response = authenticated_api_client.get(
        f'/api/image-file/{image_file_geotiff.pk}/thumbnail.png?band=1&palette=viridis'
    )
    assert response.status_code == 200
    assert response['Content-Type'] == 'image/png'
    response = authenticated_api_client.get(
        f'/api/image-file/{image_file_geotiff.pk}/thumbnail.png?band=1&palette=green&scheme=discrete'
    )
    assert response.status_code == 200
    assert response['Content-Type'] == 'image/png'


@pytest.mark.django_db(transaction=True)
def test_style_body(authenticated_api_client, image_file_geotiff):
    style = {
        'style': {
            'bands': [
                {'band': 1, 'palette': ['#000', '#0f0']},
            ]
        }
    }
    response = authenticated_api_client.get(
        f'/api/image-file/{image_file_geotiff.pk}/thumbnail.png',
        data=style,
    )
    assert response.status_code == 200
    assert response['Content-Type'] == 'image/png'
    # TODO: might want to verify style was actually used