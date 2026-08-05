# frozen_string_literal: true

class Users::OmniauthCallbacksController < Devise::OmniauthCallbacksController
  def entra
    @user = User.from_omniauth(request.env["omniauth.auth"])

    if @user.persisted?
      sign_in_and_redirect @user, event: :authentication
      set_flash_message(:notice, :success, kind: "Entra ID") if is_navigational_format?
    else
      redirect_to new_user_session_path, alert: "Unable to sign in with Entra ID"
    end
  end

  def failure
    redirect_to new_user_session_path, alert: params[:message] || "Unable to sign in with Entra ID"
  end
end
